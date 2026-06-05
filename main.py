import app
import newGCSXbee
import time

if __name__ == "__main__":

    # Initliaze Main Variables
    TEAM_ID = "1075" #TEAM_ID = "3174" # Last Year's team number
    DEVICE_FILE = "/dev/tty.usbserial-B0025E87" #MACINTOSH
    #DEVICE_FILE = "/dev/ttyUSB0" #RASP-PI
    BAUDRATE = 9600
    LOG_FILE = "./test_out.csv"
    PRESSURE_FILE = "./SIM_Pressure.csv"
    XBEE_MAC_ADDR = "0013A200427469BF" #CANSAT
    #XBEE_MAC_ADDR = "0013A200423D8F47" #TEST RADIO
    
    # Create the GUI and telemetry handler objects
    gui_app = app.App(TEAM_ID)

    # Create a telemetry handler object
    telemetry_handler = newGCSXbee.TelemetryHandler(TEAM_ID, xbee_port=DEVICE_FILE, xbee_baudrate=BAUDRATE, xbee_target_mac_addr=XBEE_MAC_ADDR, press_csv_path=PRESSURE_FILE, log_csv_path=LOG_FILE)
    
    telemetry_handler.start_telemetry()
    gui_app.mainloop()

    time.sleep(1)

    telemetry_handler.stop_telemetry()
