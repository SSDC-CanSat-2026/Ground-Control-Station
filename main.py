import app
import newGCSXbee
import time

if __name__ == "__main__":

    # Initliaze Main Variables
    TEAM_ID = "1075" #TEAM_ID = "3174" # Last Year's team number
    DEVICE_FILE = "/dev/tty.usbserial-A10KGKGP"
    BAUDRATE = 921600
    LOG_FILE = "./test.csv"
    PRESSURE_FILE = "./test.csv"
    XBEE_MAC_ADDR = "0013A20041E0613B"
    
    # Create the GUI and telemetry handler objects
    gui_app = app.App(TEAM_ID)

    # Create a telemetry handler object
    telemetry_handler = newGCSXbee.TelemetryHandler(TEAM_ID, xbee_port=DEVICE_FILE, xbee_baudrate=BAUDRATE, xbee_mac_addr=XBEE_MAC_ADDR, press_csv_path=PRESSURE_FILE, log_csv_path=LOG_FILE)
    
    telemetry_handler.start_telemetry()
    gui_app.mainloop()

    time.sleep(6)

    telemetry_handler.stop_telemetry()
