import socket
import time
import threading
import telemetryPacket
from datetime import datetime, timezone
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import enum

HOST = 'localhost'
PORT_TH = 6000
PORT_GUI = 6001
ADDRESS_TH = (HOST, PORT_TH)
ADDRESS_GUI = (HOST, PORT_GUI)
DEFAULT_PRESSURE = 101325

class Status(enum.Enum):
    DISABLED = enum.auto()
    WAITING_ENABLE = enum.auto()
    ENABLED = enum.auto()
    WAITING_ACTIVE = enum.auto()
    ACTIVE = enum.auto()
    WAITING_DISABLED = enum.auto()

class TelemetryHandler:

    def __init__(self, team_id, xbee_port, xbee_baudrate, xbee_target_mac_addr, press_csv_path=None, log_csv_path=None):

        # Load some of the init variables
        self.team_id = team_id
        self.press_csv_path = press_csv_path
        self.log_csv_path = log_csv_path

        # Operation Variables
        self.is_running = True
        self.sim_status = Status.DISABLED
        self.sim_disable_pending = False
        self.latest_pkt = False
        self.valid_xbee_connection = False
        self.valid_pressure_file = False
        self.valid_log_file = False

        # Initialize XBee connection
        self.xbee_port = xbee_port
        self.xbee_baudrate = xbee_baudrate
        self.xbee_target_mac_addr = xbee_target_mac_addr
        self.xbee_device = XBeeDevice(self.xbee_port, self.xbee_baudrate)
        self.xbee_receiver = RemoteXBeeDevice(x64bit_addr=XBee64BitAddress.from_hex_string(self.xbee_target_mac_addr), local_xbee=self.xbee_device)

    def start_telemetry(self):

        print("[DEBUG] Handler Started")

        # Open the xbee device
        try:
            self.xbee_device.open()
            self.valid_xbee_connection = True
            print(f"[DEBUG] XBee Device Open Successful: {self.xbee_port}")
        except Exception as e:
            print(f"[DEBUG] Failed to open XBee device: {e}")
            self.valid_xbee_connection = False

        # Open the pressure file
        try:
            self.press_csv_file = open(self.press_csv_path,'rt')
            self.valid_pressure_file = True
            print(f"[DEBUG] Pressure CSV Open Successful: {self.press_csv_path}")
        except Exception as e:
            print(f"[DEBUG] Failed to Open Pressure CSV File, Defaulting to {DEFAULT_PRESSURE} Pascals: {e}")
            self.press_csv_file = None
            self.valid_pressure_file = False

        # Open the log file
        try:
            self.log_csv_file = open(self.log_csv_path,'ta')
            self.valid_log_file = True
            print(f"[DEBUG] Log CSV Open Successful: {self.log_csv_path}")
        except Exception as e:
            print(f"[DEBUG] Failed to Open Log CSV File: {e}")
            self.log_csv_file = None
            self.valid_log_file = False 

        # Create the three threads, one for monitoring the incoming commands, one for running the main execution loop that sends data to the GUI, one for running the simulation loop when in simulation mode
        # Seperate threads are necessary for each operation as they needs to be "Asynchronous" because they are time sensitive
        self.forwarding_thread = threading.Thread(target=self._forwarding_loop, daemon=True)
        self.command_thread = threading.Thread(target=self._command_loop, daemon=True)
        self.simulation_thread = threading.Thread(target=self._simulation_loop, daemon=True)
        
        self.forwarding_thread.start()
        self.command_thread.start()
        self.simulation_thread.start()

        return

    def stop_telemetry(self):
        
        self.is_running = False

        self.forwarding_thread.join()
        self.command_thread.join()
        self.simulation_thread.join()

        return

    def _command_loop(self):

        sock_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_in.bind(ADDRESS_TH)
        sock_in.listen(0)
        sock_in.settimeout(2)

        while (self.is_running):
            try:
                conn, addr = sock_in.accept()
                full_data = ""
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    full_data += data.decode('utf-8')
                conn.close()
                print("[DEBUG] TLH Recv:", full_data)
                self._handle_command(full_data)
            except socket.timeout:
                #print("[DEBUG] Socket Timout")
                1==1

    def _forwarding_loop(self):

        #time.sleep(1)
        i = 1

        while (self.is_running == True):
            # Write to the socket instead 
            time.sleep(1)
            #print("[DEBUG] LOOP OUTGOING")

            if self.valid_xbee_connection:
                try:
                    if self.xbee_device.is_open():
                        xbee_message = self.xbee_device.read_data(20) # The 20 is a timeout parameter
                        if xbee_message:
                            line = xbee_message.data.decode('utf-8').strip()
                            self.latest_pkt = telemetryPacket.TelemetryPacket(line)
                            print(f"[DEBUG PACKET:]{line}\n")
                            if (self.valid_log_file):
                                self.log_csv_file.write(self.latest_pkt.get_str())

                            # Update the state of the simulator if it's in a pending state for any modes
                            if self.latest_pkt.CMD_ECHO == "SIMDIS" and self.sim_status == Status.DISABLED and self.sim_disable_pending == True:
                                self.sim_disable_pending = False
                                print("[DEBUG] FSW SIMULATION DISABLE CONFIRMED")
                            elif self.latest_pkt.CMD_ECHO == "SIMENABLE" and self.sim_status == Status.WAITING_ENABLE:
                                self.sim_status = Status.ENABLED
                                print("[DEBUG] SIMULATION NOW ENABLED")
                            elif self.latest_pkt.CMD_ECHO == "SIMACT" and self.sim_status == Status.WAITING_ACTIVE:
                                if self.latest_pkt.MODE == "S":
                                    self.sim_status = Status.ACTIVE
                                    print("[DEBUG] SIMULATION NOW ACTIVE")
                                else:
                                    print("[ERROR] FSW RECEIVED ACTIVE REQUEST BUT MODE DID NOT CHANGE")
                        else:
                            self.latest_pkt = None
                            print("[DEBUG] Xbee Device Read Timout. (Latest Packet is now \"None\")")
                    else:
                        print("[DEBUG] Packet Polling Failed, XBEE Closed")
                except Exception as e:
                    print(f"[ERROR] Xbee Device Read Error Occurred: {e}")
                    self.latest_pkt = None
                    #self.valid_xbee_connection = False

                if (self.latest_pkt and self.latest_pkt.valid_packet):
                    line = self.latest_pkt.get_str()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    if (not sock.connect_ex(ADDRESS_GUI)):    
                        sock.send(line.encode('utf-8'))
                        #print("[DEBUG] TLH Sent:", line)
                        i += 1
                    else:
                        print("[DEBUG] TLH Failed Send")
                        1==1

                    sock.close()

    def _simulation_loop(self):

        while (self.is_running == True):
            # Write to the socket instead 
            time.sleep(1)

            while (self.sim_status == Status.ACTIVE):
                if (self.valid_pressure_file):
                    temp_pressure_str = self.press_csv_file.readline()
                    temp_clean_str = temp_pressure_str.strip("\n")
                    if temp_pressure_str:
                        self._send_packet(f"CMD,1075,SIMP,{temp_clean_str}")
                        print(f"[DEBUG] Pressure Packet: {temp_clean_str}")
                        time.sleep(1)
                    else:
                        print("[DEBUG] End of Pressure File")
                        time.sleep(1)
                else:
                    #print(f"[DEBUG] NO PRESSURE FILE OPEN")
                    temp_clean_str = str(DEFAULT_PRESSURE)
                    self._send_packet(f"CMD,1075,SIMP,{temp_clean_str}")
                    print(f"[DEBUG] Pressure Packet: {temp_clean_str}")
                    time.sleep(1)

        return

    def _handle_command(self, cmd):

        str = "[DEBUG] DUMMY COMMAND PACKET"
        fields = cmd.split(",")
        cmd_field = fields[0]
        match (cmd_field):
            case "CX_ON":
                str = "CMD,1075,CX,ON"
                self._send_packet(str)
            case "CX_OFF":
                str = "CMD,1075,CX,OFF"
                self._send_packet(str)
            case "ST_UTC":
                utc_now = datetime.now(timezone.utc)
                utc_time = utc_now.strftime("%H:%M:%S")
                packet_str = f"CMD,1075,ST,{utc_time}"
                self._send_packet(packet_str)
            case "ST_GPS":
                str = "CMD,1075,ST,GPS"
                self._send_packet(str)
            case "SIM_EN":
                str = "CMD,1075,SIM,ENABLE"
                self._send_packet(str)
                match(self.sim_status):
                    case Status.DISABLED:
                        self.sim_status = Status.WAITING_ENABLE
                        print("[DEBUG] SIMULATION ENABLE NOW PENDING")
                    case Status.WAITING_ENABLE:
                        print("[DEBUG] SIMULATION ENABLE ALREADY PENDING (RESENDING)")
                    case Status.ENABLED:
                        print("[DEBUG] SIMULATION ALREADY ACTIVE")
                    case Status.WAITING_ACTIVE:
                        print("[DEBUG] SIMULATION ALREADY ACTIVE")
                    case Status.ACTIVE:
                        print("[DEBUG] SIMULATION ALREADY ENABLED AND ACTIVE")
                    case Status.WAITING_DISABLED:
                        print("[DEBUG] CAN'T ENABLE, SIMULATION DISABLE PENDING")
                    case _:
                        print("[ERROR] SIM STATUS IN INVALID STATE")
            case "SIM_ACT":
                str = "CMD,1075,SIM,ACTIVATE"
                self._send_packet(str)
                match(self.sim_status):
                    case Status.DISABLED:
                        print("[DEBUG] SIMULATION IS OFF")
                    case Status.WAITING_ENABLE:
                        print("[DEBUG] SIMULATION ENABLE STILL PENDING")
                    case Status.ENABLED:
                        self.sim_status = Status.WAITING_ACTIVE
                        print("[DEBUG] SIMULATION ACTIVE NOW PENDING")
                    case Status.WAITING_ACTIVE:
                        print("[DEBUG] SIMULATION ACTIVE ALREADY PENDING (RESENDING)")
                    case Status.ACTIVE:
                        print("[DEBUG] SIMULATION ALREADY ACTIVE")
                    case Status.WAITING_DISABLED:
                        print("[DEBUG] CAN'T ACTIVATE, SIMULATION DISABLE PENDING")
                    case _:
                        print("[ERROR] SIM STATUS IN INVALID STATE")
            case "SIM_DIS":
                if self.press_csv_file:
                    self.press_csv_file.seek(0) #Resets the the pressure file's position anytime simulation is disabled to allow reruns
                str = "CMD,1075,SIM,DISABLE"
                self._send_packet(str)
                self.sim_disable_pending = True
                match(self.sim_status):
                    case Status.DISABLED:
                        print("[DEBUG] SIMULATION IS ALREADY OFF")
                    case Status.WAITING_ENABLE:
                        self.sim_status = Status.DISABLED
                        print("[DEBUG] SIMULATION DISABLE NOW PENDING, LOCAL SIM DISABLED")
                    case Status.ENABLED:
                        self.sim_status = Status.DISABLED
                        print("[DEBUG] SIMULATION DISABLE NOW PENDING, LOCAL SIM DISABLED")
                    case Status.WAITING_ACTIVE:
                        self.sim_status = Status.DISABLED
                        print("[DEBUG] SIMULATION DISABLE NOW PENDING, LOCAL SIM DISABLED")
                    case Status.ACTIVE:
                        self.sim_status = Status.DISABLED
                        print("[DEBUG] SIMULATION DISABLE NOW PENDING, LOCAL SIM DISABLED")
                    case _:
                        print(f"[ERROR] SIM STATUS IN INVALID STATE {self.sim_status}, SET TO DISABLED")
                        self.sim_status = Status.DISABLED
            case "CAL":
                str = "CMD,1075,CAL"
                self._send_packet(str)
            case "MEC":
                if len(fields) >= 3:
                    str = f"CMD,1075,MEC,{fields[1]},{fields[2]}"
                    #print(f"[DEBUG] MECH COMMAND: {fields}")
                    self._send_packet(str)
                else:
                    print("[ERROR] INVALID MECH FORMAT RECEIVED")
            # Fake commands
            case "*REOPEN_RADIO":
                if (self.xbee_device):
                    self.xbee_device.close()
                # Re-open the xbee device
                try:
                    self.xbee_device.open()
                    self.valid_xbee_connection = True
                    print(f"[DEBUG] XBee Device Re-open Successful: {self.xbee_port}")
                except Exception as e:
                    print(f"[DEBUG] Failed to Re-open XBee device: {e}")
                    self.valid_xbee_connection = False
            case "*REOPEN_PRESSURE":
                if (self.press_csv_file):
                    self.press_csv_file.close()
                self.valid_pressure_file = False
                # Re-open the pressure file
                try:
                    self.press_csv_file = open(self.press_csv_path,'rt')
                    self.valid_pressure_file = True
                    print(f"[DEBUG] Pressure CSV Re-open Successful: {self.press_csv_path}")
                except Exception as e:
                    print(f"[DEBUG] Failed to Re-open Pressure CSV File: {e}")
                    self.valid_pressure_file = False
            case "*REOPEN_LOG":
                if (self.log_csv_file):
                    self.log_csv_file.close()
                self.valid_log_file = False
                # Re-open the log file
                try:
                    self.log_csv_file = open(self.log_csv_path,'ta')
                    self.valid_log_file = True
                    print(f"[DEBUG] Log CSV Re-open Successful: {self.log_csv_path}")
                except Exception as e:
                    print(f"[DEBUG] Failed to Re-open Log CSV File: {e}")
                    self.valid_log_file = False 
            case "*DEACTIVATE_PRESSURE":
                if (self.press_csv_file):
                    self.press_csv_file.close()
                self.valid_pressure_file = False
                print(f"[DEBUG] Closed Pressure CSV File, Defaulting to {DEFAULT_PRESSURE} Pascals")
            case _:
                print("[DEBUG] INVALID COMMAND RECEIVED")

        return

    def _send_packet(self, str):
        #print("DEBUG BLAHHHHHHHHH")
        if self.valid_xbee_connection:
            #print("DEBUG BLEHHHHHHHHH")
            try:
                if self.xbee_device.is_open():
                    #print("BLOHHHHHHH")
                    self.xbee_device.send_data_async(remote_xbee=self.xbee_receiver, data=str)
                    print(f"[DEBUG] CMD: \"{str}\" Sent")
                else:
                    print("[DEBUG] Packet Sending Failed, XBEE Closed")
            except Exception as e:
                print(f"[ERROR] Can't send packet: {e}")
