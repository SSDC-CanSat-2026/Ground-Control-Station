from app import App
import GCSXbee

if __name__ == "__main__":

    TEAM_ID = "1075"
    #TEAM_ID = "3174" # Last Year's team number

    gui_app = App(TEAM_ID)

    # Create a telemetry handler object
    telemetry_handler = None
    try:
        telemetry_handler = GCSXbee.TelemetryHandler(TEAM_ID, port="/dev/tty.usbserial-A10KGKGP", baudrate=921600, write_path="./test.csv", mac_addr="0013A20041E060D2")
        telemetry_handler.start_telemetry()
    except Exception as e:
        print(e)

    #gui_app.demo_graph_print()

    gui_app.my_telemetry_handler = telemetry_handler

    gui_app.mainloop()

    telemetry_handler.stop_telemetry()