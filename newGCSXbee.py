import socket
import time
import threading

HOST = 'localhost'
PORT_TH = 6000
PORT_GUI = 6001
ADDRESS_TH = (HOST, PORT_TH)
ADDRESS_GUI = (HOST, PORT_GUI)

class TelemetryHandler:

    def __init__(self, team_id, xbee_port, xbee_baudrate, xbee_mac_addr, press_csv_path=None, log_csv_path=None):

        # Global Variables that keeps the threads running
        self.is_running = True

        # Load all the given variables
        self.team_id = team_id

        # Operation Variables
        self.sim_active = False

        

    def start_telemetry(self):

        print("Handler Started")

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
                print("PROC Recv:", full_data)
            except socket.timeout:
                #print("Socket Timout")
                1==1

    def _forwarding_loop(self):

        #time.sleep(1)
        i = 1

        while (self.is_running == True):
            # Write to the socket instead 
            time.sleep(1)
            #print("LOOP OUTGOING")

            line = str(i)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if (not sock.connect_ex(ADDRESS_GUI)):    
                sock.send(line.encode('utf-8'))
                print("Proc Sent:", line)
                i += 1
            else:
                #print("Proc Failed Send")
                1==1

            sock.close()

    def _simulation_loop(self):

        while (self.is_running == True):

            if (self.sim_active):
                1==1
        return


'''
import csv
import socket
import os
import time
from threading import Thread
from datetime import datetime, timezone
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

address = ('localhost', 6000)

class TelemetryHandler:
    
    def _receive_command(self):

        print("HELLO!")

        address = ('localhost', 6001)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(address)
        sock.listen(0)

        # Set up the client connection
        client_socket, client_address = sock.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        # Read in a message from the client
        msg = client_socket.recv(1024)
        msg = msg.decode("utf-8") # convert bytes to string

        # Update the Tkinter text widget with received data
        print(f"Received: {msg}")

        # Close the connection
        client_socket.close()
    
    def __init__(self, team_id, port="COM3", baudrate=9600, write_path=None, mac_addr="0013A20041E060D1"): # default port val for Fernando's laptop

        ##################### File path for the simulated data to be used #####################
        self.SIM_CSV_PATH = "SIM_Pressure.csv"  # Path to the simulated data CSV file
        #######################################################################################

        # Some of these definitions are redundant, but they are here for clarity
        self.team_id = team_id
        self.is_receiving = False
        self.csv_file = None
        self.csv_writer = None
        self.packet_count = 0
        self.sim_enable = False
        self.sim_activate = False
        self.simulation_thread = None
        self.receiver = None
        self.write_filepath = write_path
        if self.write_filepath == None:
            raise Exception(f"GCSXbee (File: GCSXbee.py Function: __init__) [INITIALIZATION] : No file write_path given")

        # Define telemetry fields as per competition requirements
        self.telemetry_fields = ["TEAM_ID","MISSION_TIME","PACKET_COUNT","MODE","STATE","ALTITUDE",
              "TEMPERATURE", "PRESSURE", "VOLTAGE","CURRENT",
              "GYRO_R", "GYRO_P", "GYRO_Y", "ACCEL_R", "ACCEL_P", "ACCEL_Y",
              "GPS_TIME", "GPS_ALTITUDE", "GPS_LATITUDE", "GPS_LONGITUDE", "GPS_SATS", "CMD_ECHO"]

        # Initialize XBee connection
        self.mac_address = mac_addr # This is the MAC address of the FSW radio (the one on the Sat)
        self.xbee_device = XBeeDevice(port, baudrate)
        self.receiver = RemoteXBeeDevice(x64bit_addr=XBee64BitAddress.from_hex_string(self.mac_address), local_xbee=self.xbee_device)
        # FIXME : This MAC address will need to be updated to the actual FSW radio's MAC address

    def start_telemetry(self):
        """Start receiving telemetry data."""
        
        self.command_thread = Thread(target=self._receive_command, daemon=True)
        self.command_thread.start()

        self.receive_thread = None
        
        try:
            self.xbee_device.open()
        except Exception as e:
            raise Exception(f"GCSXbee (File: GCSXbee.py Function: start_telemetry) [START TELEMETRY] Failed to open XBee device: {e}")
            return # Prevents the .csv from being overwritten. Should have done this sooner.
        
        # FIXME:
        # Create CSV file with specified naming format
        #self.csv_file = open(self.write_filepath, 'w', newline='')
        #self.csv_writer = csv.writer(self.csv_file)

        # Write header row
        #self.csv_writer.writerow(self.telemetry_fields)

        # Start receiving data
        self.is_receiving = True
        self.receive_thread = Thread(target=self._receive_telemetry, daemon=True)
        self.receive_thread.start()

    def stop_telemetry(self):
        """Stop receiving telemetry data and close files."""
        self.is_receiving = False
        if self.receive_thread:
            self.receive_thread.join()
        if self.command_thread:
            self.command_thread.join()

        # FIXME:
        #if self.csv_file:
        #    self.csv_file.close()

        print(f"GCSXbee (File: GCSXbee.py Function: stop_telemetry) [STOP TELEMETRY] : Telemetry stopped. {self.packet_count} packets received.")

        # if self.xbee_device and self.xbee_device.is_open():
        #     self.send_command(f"CMD,{self.team_id},CX,OFF")
        #     self.xbee_device.close()

    def send_command(self, command):
        """
        Send a command to the CanSat.

        Args:
            command (str): Command string following competition format.
        """

        # Because the FSW uses a buffer to help read the commands sent to it, if the buffer is not filled right away it will wait until it is filled.
        # This will cause some commands to need to be sent twice. Padding the strings here with null terms allows the commands to be sent once.
        if command == "CX ON":
            print("[DEBUG] CX-ON COMMAND ENTERED") #FIXME: REMOVE
            CXON = f"CMD,{self.team_id},CX,ON\0\0\0\0\0\0\0\0"
            try:
                print("[DEBUG] CX-ON COMMAND INSIDE") #FIXME: REMOVE
                if self.xbee_device.is_open():
                    self.xbee_device.send_data_async(remote_xbee=self.receiver, data=CXON)
                    print("[DEBUG] CX-ON COMMAND SUCCESS") #FIXME: REMOVE
                else:
                    print("[DEBUG] CX-ON COMMAND FAILED") #FIXME: REMOVE
            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: send_command) [COMMAND CXON]: Error sending command - {e}")

        elif command == "CX OFF":
            print("[DEBUG] CX-OFF COMMAND ENTERED") #FIXME: REMOVE
            CXOFF = f"CMD,{self.team_id},CX,OFF\0\0\0\0\0\0\0"
            try:
                print("[DEBUG] CX-OFF COMMAND INSIDE") #FIXME: REMOVE
                if self.xbee_device.is_open():
                    self.xbee_device.send_data_async(remote_xbee=self.receiver ,data=CXOFF)
                    print("[DEBUG] CX-OFF COMMAND SUCCESS") #FIXME: REMOVE
                else:
                    print("[DEBUG] CX-OFF COMMAND FAILED") #FIXME: REMOVE
            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: send_command) [COMMAND CXOFF]: Error sending command - {e}")
        
        elif command == "SIM ENABLE":
            ENABLE = f"CMD,{self.team_id},SIM,ENABLE\0\0\0"
            try:
                if self.xbee_device.is_open():
                    self.xbee_device.send_data_async(remote_xbee=self.receiver, data=ENABLE)
            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: send_command) [COMMAND SIM ENABLE]: Error sending command - {e}")

        elif command == "SIM ACTIVATE":
            ACTIVATE = f"CMD,{self.team_id},SIM,ACTIVATE\0"
            try:
                if self.xbee_device.is_open() and self.sim_enable:
                    self.xbee_device.send_data_async(remote_xbee=self.receiver, data=ACTIVATE)
            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: send_command) [COMMAND SIM ACTIVATE]: Error sending command - {e}")
        
        elif command == "SIM DISABLE":
            DISABLE = f"CMD,{self.team_id},SIM,DISABLE\0\0"
            try:
                if self.xbee_device.is_open():
                    self.xbee_device.send_data_async(remote_xbee=self.receiver, data=DISABLE)
            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: send_command) [COMMAND SIM DISABLE]: Error sending command - {e}")

        elif command == "CAL":
            CAL = f"CMD,{self.team_id},CAL\0\0\0\0\0\0\0\0\0\0"
            print(f"Sending command: {CAL}")
            try:
                if self.xbee_device.is_open():
                    self.xbee_device.send_data_async(remote_xbee=self.receiver, data=CAL)
            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: send_command) [COMMAND CAL]: Error sending command - {e}")

        elif command == "ST GPS":
            ST_GPS = f"CMD,{self.team_id},ST,GPS\0\0\0\0\0\0\0"
            try:
                if self.xbee_device.is_open():
                    self.xbee_device.send_data_async(remote_xbee=self.receiver, data=ST_GPS)
            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: send_command) [COMMAND ST GPS]: Error sending command - {e}")

        elif command[0:2] == "ST":
            current_time = "00:00:00"
            try: # This is just a bunch of handling I did in case the user gives an incomplete cmd, probably not necessary but is nice to have.
                current_time = command[3:]
                if current_time == "":
                    current_time = datetime.now(timezone.utc).strftime('%H:%M:%S')
                elif len(current_time) != 8:
                    current_time = datetime.now(timezone.utc).strftime('%H:%M:%S')
                elif current_time.count(":") != 2:
                    current_time = datetime.now(timezone.utc).strftime('%H:%M:%S')
                elif current_time[2] != ":" or current_time[5] != ":":
                    current_time = datetime.now(timezone.utc).strftime('%H:%M:%S')
                elif int(current_time[0:2]) > 23 or int(current_time[3:5]) > 59 or int(current_time[6:8]) > 59:
                    current_time = datetime.now(timezone.utc).strftime('%H:%M:%S')
            
            except:
                current_time = datetime.now(timezone.utc).strftime('%H:%M:%S') # Get the current time in UTC
            print(current_time)
            ST = f"CMD,{self.team_id},ST,{current_time}\0\0"
            print(ST)
            try:
                if self.xbee_device.is_open():
                    self.xbee_device.send_data_async(remote_xbee=self.receiver, data=ST)
            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: send_command) [COMMAND ST]: Error sending command - {e}")

        elif command == "MEC WIRE ON":
            MEC_WIRE = f"CMD,{self.team_id},MEC,WIRE,ON\0\0"
            try:
                if self.xbee_device.is_open():
                    self.xbee_device.send_data_async(remote_xbee=self.receiver, data=MEC_WIRE)
            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: send_command) [COMMAND MEC WIRE ON]: Error sending command - {e}")

        elif command == "MEC WIRE OFF":
            MEC_WIRE = f"CMD,{self.team_id},MEC,WIRE,OFF\0"
            try:
                if self.xbee_device.is_open():
                    self.xbee_device.send_data_async(remote_xbee=self.receiver, data=MEC_WIRE)
            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: send_command) [COMMAND MEC WIRE OFF]: Error sending command - {e}")

        # FIXME : Add any other MEC commands here -------------------------------------------------------------------------------

        else:
            print(f"ERROR (File: GCSXbee.py Function: send_command) [SEND_COMMAND]: Unknown command - {command}")

    def _receive_telemetry(self):
        """Internal method to receive and process telemetry data."""
        while self.is_receiving:
            try:
                xbee_message = self.xbee_device.read_data(20) # The 20 is a timeout parameter
                if xbee_message:
                    # Read and decode the message
                    line = xbee_message.data.decode('utf-8').strip()
                    xbee_message = self.xbee_device.read_data(20)  # Read the next message
                    if xbee_message is None:
                        continue
                    line = line + xbee_message.data.decode('utf-8').strip()  # Append the next message data
                    #print(f"[RECEIVE TELEMETRY] Received - [{line}]") #FIXME: Remove this later
                    data = line.split(',')

                    # Because we could not get the GPS to work, we have to fake all of the GPS data.
                    # This includes GPS time, but it is easier to do that here in the GCS. Whoopsies.
                    #current_time = datetime.now(timezone.utc).strftime('%H:%M:%S')
                    #data[19] = current_time

                    # Validate team ID and basic data format
                    if (len(data) >= len(self.telemetry_fields)) and (data[0] == self.team_id):
                        
                        # FIXME: DO some formatting later
                        # Write to CSV file
                        #self.csv_writer.writerow(data)
                        #self.csv_file.flush()  # Ensure data is written to disk

                        # Write to the socket instead 
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect(address)
                        sock.send(line.encode('utf-8'))
                        print("Sent:",line)
                        sock.close()

                        # Update packet count
                        self.packet_count += 1

                    # # FIXME : This may need to be updated to handle the format that FSW sends us (the array index that is) -------------------------
                    # if data[24] == "SIMENABLE":
                    #     self.sim_enable = True

                    # elif data[24] == "SIMACT":
                    #     self.sim_activate = True 
                    #     self.start_sim()                     

                    # elif data[24] == "SIMDIS":
                    #     self.sim_activate = False
                    #     self.sim_enable = False
                    #     if self.simulation_thread:
                    #         self.stop_sim()

            except Exception as e:
                print(f"ERROR (File: GCSXbee.py Function: _receive_telemetry) [RECEIVE TELEMETRY] : {e}")

    def start_sim(self):
        if (self.sim_enable and self.sim_activate):
            print(self.SIM_CSV_PATH)
            self.simulation_thread = Thread(target=self._send_command_pressure)
            self.simulation_thread.start()

    def stop_sim(self):
        """
        Stop sending simulated pressure data.
        """
        # while self.simulation_thread:
        print("Waiting for simulation thread to finish...")
        self.simulation_thread.join()

        self.sim_enable = False
        self.sim_activate = False
        print("Simulation stopped.")

    def _send_command_pressure(self):
        """
        Send simulated pressure data (simulation mode only).

        Args:
            csv_path (string): Path to the CSV file containing pressure data.
        """
        
        with open(self.SIM_CSV_PATH, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if not self.sim_enable or not self.sim_activate: # Check if simulation is enabled and activated
                    print("Simulation disabled or not activated. Stopping simulation thread.")
                    break
                DATA = f"CMD,{self.team_id},SIMP,{row[0]}"
                self.xbee_device.send_data_async(remote_xbee=self.receiver, data=DATA)
                time.sleep(1)

        DATA = f"CMD,{self.team_id},SIM,DISABLE";
        self.xbee_device.send_data_async(remote_xbee=self.receiver, data=DATA)
        print("Simulation thread finished.")

# Initliaze Main Variables
TEAM_ID = "1075" #TEAM_ID = "3174" # Last Year's team number
DEVICE_FILE = "/dev/tty.usbserial-A10KGKGP"
BAUDRATE = 921600
LOG_FILE = "./test.csv"
XBEE_MAC_ADDR = "0013A20041E0613B"

# Create a telemetry handler object
telemetry_handler = None
try:
    telemetry_handler = TelemetryHandler(TEAM_ID, port=DEVICE_FILE, baudrate=BAUDRATE, write_path=LOG_FILE, mac_addr=XBEE_MAC_ADDR)
    telemetry_handler.start_telemetry()
except Exception as e:
    print(e)

telemetry_handler.stop_telemetry()
'''