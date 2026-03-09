from app import App
import GCSXbee

if __name__ == "__main__":

    # Initliaze Main Variables
    TEAM_ID = "1075" #TEAM_ID = "3174" # Last Year's team number
    DEVICE_FILE = "/dev/tty.usbserial-A10KGKGP"
    BAUDRATE = 921600
    LOG_FILE = "./test.csv"
    XBEE_MAC_ADDR = "0013A20041E0613B"
    
    # Create the GUI and telemetry handler objects
    gui_app = App(TEAM_ID)

    # Create a telemetry handler object
    telemetry_handler = None
    try:
        telemetry_handler = GCSXbee.TelemetryHandler(TEAM_ID, port=DEVICE_FILE, baudrate=BAUDRATE, write_path=LOG_FILE, mac_addr=XBEE_MAC_ADDR)
        telemetry_handler.start_telemetry()
    except Exception as e:
        print(e)

    #gui_app.demo_graph_print()

    gui_app.my_telemetry_handler = telemetry_handler

    gui_app.mainloop()

    telemetry_handler.stop_telemetry()
