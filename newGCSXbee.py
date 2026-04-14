import socket
import time
import threading
import telemetryPacket
from datetime import datetime, timezone
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

HOST = 'localhost'
PORT_TH = 6000
PORT_GUI = 6001
ADDRESS_TH = (HOST, PORT_TH)
ADDRESS_GUI = (HOST, PORT_GUI)

class TelemetryHandler:

    def __init__(self, team_id, xbee_port, xbee_baudrate, xbee_target_mac_addr, press_csv_path=None, log_csv_path=None):

        # Load some of the init variables
        self.team_id = team_id
        self.press_csv_path = press_csv_path

        # Operation Variables
        self.is_running = True
        self.sim_active = False
        self.sim_pending = False
        self.latest_pkt = False
        self.valid_xbee_connection = False
        self.valid_pressure_file = False

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
            print(f"[DEBUG] Failed to open pressure csv file: {e}")
            self.valid_pressure_file = False

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
                        print("[DEBUG] THL Sent:", line)
                        i += 1
                    else:
                        print("[DEBUG] THL Failed Send")
                        1==1

                    sock.close()

    def _simulation_loop(self):

        while (self.is_running == True):

            if (self.sim_pending):
                self.sim_active = True
                self.sim_pending = False
                self._send_packet("CMD,1075,SIM,ACTIVATE")
                print("[DEBUG] SIMULATION NOW ACTIVE")
                time.sleep(1)
                continue

            if (self.sim_active):
                if (self.valid_pressure_file):
                    temp_pressure_str = self.press_csv_file.readline()
                    temp_clean_str = temp_pressure_str.strip("\n")
                    if temp_pressure_str:
                        self._send_packet(f"CMD,1075,SIMP,{temp_clean_str}")
                        print(f"[DEBUG] Pressure Packet: {temp_clean_str}")
                        time.sleep(1)
                    else:
                        print("[DEBUG] End of Pressure File") #FIXME: MAKE IT SO THAT THE FILE RESETS POSITION WHEN THE SIMULATION IS DISABLED
                        time.sleep(1)

        return

    def _handle_command(self, cmd):

        str = "[DEBUG] DUMMY COMMAND PACKET"
        match (cmd):
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
                if (not self.sim_active and not self.sim_pending):
                    self.sim_pending = True
                    print("[DEBUG] SIMULATION NOW PENDING")
                    if (not self.valid_pressure_file):
                        print(f"[DEBUG] NO PRESSURE FILE OPEN")
                    else:
                        self.press_csv_file.seek(0)
                elif (self.sim_pending):
                    print("[DEBUG] SIMULATION ALREADY PENDING")
                elif (self.sim_active):
                    print("[DEBUG] SIMULATION ALREADY ACTIVE")
            case "SIM_DIS":
                str = "CMD,1075,SIM,DISABLE"
                self._send_packet(str)
                if (self.sim_active):
                    print("[DEBUG] SIMULATION NOW OFF")
                else:
                    print("[DEBUG] SIMULATION ALREADY OFF")
                self.sim_active = False
                self.sim_pending = False
            case "CAL":
                str = "CMD,1075,CAL"
                self._send_packet(str)
            case _:
                print("[DEBUG] INVALID COMMAND RECEIVED")

        return

    def _send_packet(self, str):
        #print("DEBUG BLAHHHHHHHHH")
        if self.valid_xbee_connection:
            #print("DEBUG BLEHHHHHHHHH")
            try:
                if self.xbee_device.is_open():
                    print("BLAHHHHHHH")
                    self.xbee_device.send_data_async(remote_xbee=self.xbee_receiver, data=str)
                else:
                    print("[DEBUG] Packet Sending Failed, XBEE Closed")
            except Exception as e:
                print(f"[ERROR] Can't send packet: {e}")
