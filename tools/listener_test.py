import tkinter as tk
import socket
import GCSXbee

class TelemetryPacket:
    TEAM_ID = ""
    MISSION_TIME = ""
    PACKET_COUNT = ""
    MODE = ""
    STATE = ""
    ALTITUDE = ""
    TEMPERATURE = ""
    PRESSURE = ""
    VOLTAGE = ""
    CURRENT = ""
    GYRO_R = ""
    GYRO_P = ""
    GYRO_Y = ""
    ACCEL_R = ""
    ACCEL_P = ""
    ACCEL_Y = ""
    GPS_TIME = ""
    GPS_ALTITUDE = ""
    GPS_LATITUDE = ""
    GPS_LONGITUDE = ""
    GPS_SATS = ""
    CMD_ECHO = ""

    def __init__(self, string):
        fields = string.split(",")
        
        self.TEAM_ID = fields[0]
        self.MISSION_TIME = fields[1]
        self.PACKET_COUNT = fields[2]
        self.MODE = fields[3]
        self.STATE = fields[4]
        self.ALTITUDE = fields[5]
        self.TEMPERATURE = fields[6]
        self.PRESSURE = fields[7]
        self.VOLTAGE = fields[8]
        self.CURRENT = fields[9]
        self.GYRO_R = fields[10]
        self.GYRO_P = fields[11]
        self.GYRO_Y = fields[12]
        self.ACCEL_R = fields[13]
        self.ACCEL_P = fields[14]
        self.ACCEL_Y = fields[15]
        self.GPS_TIME = fields[16]
        self.GPS_ALTITUDE = fields[17]
        self.GPS_LATITUDE = fields[18]
        self.GPS_LONGITUDE = fields[19]
        self.GPS_SATS = fields[20]
        self.CMD_ECHO = fields[21]

    def get_str(self):

        return f"{self.TEAM_ID},{self.MISSION_TIME},{self.PACKET_COUNT},{self.MODE},{self.STATE},{self.ALTITUDE},{self.TEMPERATURE},{self.PRESSURE},{self.VOLTAGE},{self.CURRENT},{self.GYRO_R},{self.GYRO_P},{self.GYRO_Y},{self.ACCEL_R},{self.ACCEL_P},{self.ACCEL_Y},{self.GPS_TIME},{self.GPS_ALTITUDE},{self.GPS_LATITUDE},{self.GPS_LONGITUDE},{self.GPS_SATS},{self.CMD_ECHO}"


address = ('localhost', 6000)

# Create the main window
root = tk.Tk()
root.title("Asynchronous Socket Listening Test")
root.rowconfigure(0, weight=1, uniform='a')
root.columnconfigure(0, weight=1, uniform='a')
# Create and attach label
label_message = tk.Label(root, text="[NO MESSAGE]", background="white", font=("", 50, "bold"), wraplength= root.winfo_screenwidth() * 0.9, justify=tk.LEFT) # Align text to the left)
label_message.grid(row = 0, column = 0, columnspan = 1, rowspan=1, sticky="nw")

# Cross Compatible Zoom
try:
    root.wm_attributes("-zoomed",True) # Linux Version of Zoom
except tk.TclError:
    root.state('zoomed') # Default to the Windows Zoom if the linux fails

# This callback function currently only reads one packet before closing the client connection so the client has to re-connect for every packet sent
def recv_msg_callback(sock, mask):
    
    # Set up the client connection
    client_socket, client_address = sock.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # Read in a message from the client
    msg = client_socket.recv(1024)
    msg = msg.decode("utf-8") # convert bytes to string

    # Update the Tkinter text widget with received data
    label_message.config(text=msg)
    print(f"Received: {msg}")

    pkt = TelemetryPacket(msg)
    print(f"Team ID: {pkt.TEAM_ID}")
    print(f"Mission Time: {pkt.MISSION_TIME}")
    print(f"Packet Cnt: {pkt.PACKET_COUNT}")
    print(f"Mode: {pkt.MODE}")
    print(f"State: {pkt.STATE}")
    print(f"Altitude: {pkt.ALTITUDE}")
    print(f"Temperature: {pkt.TEMPERATURE}")
    print(f"Pressure: {pkt.PRESSURE}")
    print(f"...")


    # Close the connection
    client_socket.close()

# Create the Socket Object and bind it as well as add it to the tkinter event system
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(address)
sock.listen(0)
root.tk.createfilehandler(sock, tk.READABLE | tk.WRITABLE, recv_msg_callback)

# Create a telemetry handler object
telemetry_handler = None
try:
    telemetry_handler = GCSXbee.TelemetryHandler("3174", port="/dev/tty.usbserial-A10KGKGP", baudrate=9600, write_path="./test.csv", mac_addr="0013A20041E060D2")
    telemetry_handler.start_telemetry()
except Exception as e:
    print(e)

# Start the Tkinter event loop
root.mainloop()

# Delete the filehandler and close the socket connection on the way out
root.tk.deletefilehandler(sock)
sock.close()

telemetry_handler.stop_telemetry()