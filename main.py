from app import App
import GCSXbee

if __name__ == "__main__":
    gui_app = App()
    #gui_app.hi_loop_callback()

    #gui_app.demo_loop_callback()

    # Create a telemetry handler object
    telemetry_handler = None
    try:
        telemetry_handler = GCSXbee.TelemetryHandler("3174", port="/dev/tty.usbserial-A10KGKGP", baudrate=9600, write_path="./test.csv", mac_addr="0013A20041E060D2")
        telemetry_handler.start_telemetry()
    except Exception as e:
        print(e)

    gui_app.mainloop()

    telemetry_handler.stop_telemetry()