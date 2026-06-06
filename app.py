# Libraries and Packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import socket
import telemetryPacket
import platform

########################## Global Variables ##########################

# Colors and Fonts for Blue and Orange Theme
global COLOR_BG_GRAY;           COLOR_BG_GRAY = '#F0F0F0'               # Light gray
#global COLOR_BG_CREAM;           COLOR_BG_CREAM = '#FFF7F0'               # Light Orange
global COLOR_GATOR_ORANGE;      COLOR_GATOR_ORANGE = "#FA4616"          # Gator Orange
global COLOR_GATOR_BLUE;        COLOR_GATOR_BLUE = "#0021A5"            # Gator Blue
global COLOR_GATOR_GREEN;       COLOR_GATOR_GREEN = "#22884C"           # Gator Green
global COLOR_SSDC_NAVY;         COLOR_SSDC_NAVY = "#001F3C"             # SSDC Navy Blue
global COLOR_FADED_TEXT;        COLOR_FADED_TEXT = "#929292"            # Mute gray
global FONT_TITLE;              FONT_TITLE = ("Verdana", 16, "bold")
global FONT_MENU;               FONT_MENU = ("Verdana", 14, "bold")
global FONT_TEXT_BOLD;          FONT_TEXT_BOLD = ("Verdana", 14, "bold")
global FONT_TEXT_BOLD_UNDER;    FONT_TEXT_BOLD_UNDER = ("Verdana", 14, "bold", "underline")
global FONT_DEBUG;              FONT_DEBUG = ("Verdana", 16, "bold")

HOST = 'localhost'
PORT_TH = 6000
PORT_GUI = 6001
ADDRESS_TH = (HOST, PORT_TH)
ADDRESS_GUI = (HOST, PORT_GUI)

######################################################################

class App(tk.Tk):

    graph_data = [
        list([]),    # altitude
        list([]),    # voltage
        list([]),    # current
        list([]),    # accel_r
        list([]),    # accel_p
        list([]),    # accel_y
        list([]),    # gyro_r
        list([]),    # gyro_p
        list([])     # gyro_y
    ]
    graph_domain = list([])     # sample number
    gps_data = [
        list([]),   #latitude
        list([]),   #longitude
        list([])    #altitude
    ]

    def __init__(self, TEAM_ID):

        print("[DEBUG] GUI Started")

        # Add the TEAM_ID to the global variables
        self.TEAM_ID = TEAM_ID

        # Make all the readout variables
        self.latest_pkt = telemetryPacket.TelemetryPacket(f"{self.TEAM_ID},{'--:--:--'},{0},{'DANCE'},{'F(LORIDA)'},{''},{'WARM'},{''},{''},{''},{''},{''},{''},{''},{''},{''},{''},{1},{2},{3},{''},{''}")
        self.int_packet_rcv = int(self.latest_pkt.PACKET_COUNT)
        self.int_packet_loss = 0
        self.int_cmd_entry_state = 0
        self.my_telemetry_handler = None
        self.simulation_active = False
        self.latest_sent_command = 'ROLL_OVER'

        # Create the main window
        super().__init__()

        # Add the color and size properties to the main window
        self.title("UF SSDC Ground Control Station (Tkinter) 2025-2026")
        self.configure(bg=COLOR_BG_GRAY)
        width = self.winfo_screenwidth() # Gets the screen dimensions
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width/2, height)) # Sets the dimensions of the window to those screen dimensions

        # Set the window to default to maximized
        if platform.system() == "Linux":
            self.attributes('-zoomed', True)
        else:
            self.state('zoomed')

        # Create a toggle function for fullscreen
        def toggle_fullscreen_func(event=None):
            # Check the current status and invert it
            current_state = self.attributes('-fullscreen')
            self.attributes('-fullscreen', not current_state)

        # Start the window in fullscreen
        self.attributes('-fullscreen', True)
        self.bind('<F11>', toggle_fullscreen_func)

        # Create the main menubar and assign as the root's menu
        menubar = tk.Menu(self)
        self.config(menu=menubar) # Attach the menubar to the root window

        # Create menu bar objects
        menu_file = tk.Menu(menubar, tearoff=False)
        menu_options = tk.Menu(menubar, tearoff=False)
        menu_food = tk.Menu(menubar, tearoff=False)
        menu_commands = tk.Menu(menubar, tearoff=False)
        menu_help = tk.Menu(menubar, tearoff=False)

        # Create tabs from those objects
        menubar.add_cascade(label="File", menu=menu_file, font=FONT_MENU, underline=0) # TODO: Add a view csv button
        menubar.add_cascade(label="Options", menu=menu_options, font=FONT_MENU, underline=0)
        menubar.add_cascade(label="Food", menu=menu_food, font=FONT_MENU, underline=3)
        menubar.add_cascade(label="CMD", menu=menu_commands, font=FONT_MENU, underline=0)
        menubar.add_cascade(label="Help", menu=menu_help, font=FONT_MENU, underline=0)

        # Tack functions to those tabs 
        menu_file.add_command(label="Exit", command=self._menuFunc_exit, font=FONT_MENU, underline=0)
        menu_file.add_command(label="Reopen XBEE Radio", command=lambda:self._send_command("*REOPEN_RADIO"), font=FONT_MENU, underline=0)
        menu_file.add_command(label="Reopen Pressure File", command=lambda:self._send_command("*REOPEN_PRESSURE"), font=FONT_MENU, underline=0)
        menu_file.add_command(label="Reopen Log File", command=lambda:self._send_command("*REOPEN_LOG"), font=FONT_MENU, underline=0)
        menu_file.add_command(label="Close Pressure File", command=lambda:self._send_command("*DEACTIVATE_PRESSURE"), font=FONT_MENU, underline=0)
        menu_options.add_command(label="Reset 3D Graph Rotation", command=self._menuFunc_reset_3d, font=FONT_MENU, underline=0)
        menu_food.add_command(label="Burger", command=self._menuFunc_burger, font=FONT_MENU, underline=0)
        menu_food.add_command(label="Fries", command=self._menuFunc_fries, font=FONT_MENU, underline=0)
        menu_food.add_command(label="HotDog", command=self._menuFunc_dog, font=FONT_MENU, underline=0)
        menu_commands.add_command(label="CX ON", command=lambda:self._send_command("CX_ON"), font=FONT_MENU) # TODO: Extend the text with a mini description
        menu_commands.add_command(label="CX OFF", command=lambda:self._send_command("CX_OFF"), font=FONT_MENU)
        menu_commands.add_command(label="SET TIME UTC", command=lambda:self._send_command("ST_UTC"), font=FONT_MENU)
        menu_commands.add_command(label="SET TIME GPS", command=lambda:self._send_command("ST_GPS"), font=FONT_MENU)
        menu_commands.add_command(label="SIM ENABLE", command=lambda:self._send_command("SIM_EN"), font=FONT_MENU)
        menu_commands.add_command(label="SIM ACTIVATE", command=lambda:self._send_command("SIM_ACT"), font=FONT_MENU)
        menu_commands.add_command(label="SIM DISABLE", command=lambda:self._send_command("SIM_DIS"), font=FONT_MENU)
        menu_commands.add_command(label="CALIBRATE", command=lambda:self._send_command("CAL"), font=FONT_MENU)
        menu_commands.add_command(label="GNC ACTIVATE", command=lambda:self._send_command("GNC_ACT"), font=FONT_MENU)
        menu_help.add_command(label="About", command=self._menuFunc_about, font=FONT_MENU, underline=0)

        # Create the sub menu bar for the mech commands
        menu_mech_commands = tk.Menu(menu_commands, tearoff=False)
        # Create the tabs for the mech commands
        menu_commands.add_cascade(label="MECH COMMAND(S)", menu=menu_mech_commands, font=FONT_MENU, underline=0)
        
        # Create the sub sub menu bar(s) for the devices
        menu_servo0_commands = tk.Menu(menu_mech_commands, tearoff=False)
        menu_servo1_commands = tk.Menu(menu_mech_commands, tearoff=False)
        menu_servo2_commands = tk.Menu(menu_mech_commands, tearoff=False)
        menu_servo3_commands = tk.Menu(menu_mech_commands, tearoff=False)
        menu_servo4_commands = tk.Menu(menu_mech_commands, tearoff=False)
        menu_egg_commands = tk.Menu(menu_mech_commands, tearoff=False)
        menu_release_commands = tk.Menu(menu_mech_commands, tearoff=False)
        menu_guidance_commands = tk.Menu(menu_mech_commands, tearoff=False)
        menu_camera0_commands = tk.Menu(menu_mech_commands, tearoff=False)
        menu_camera1_commands = tk.Menu(menu_mech_commands, tearoff=False)

        # Create the tabs for the devices in the mech commands menu
        menu_mech_commands.add_cascade(label="SERVO0", menu=menu_servo0_commands, font=FONT_MENU, underline=5)
        menu_mech_commands.add_cascade(label="SERVO1", menu=menu_servo1_commands, font=FONT_MENU, underline=5)
        menu_mech_commands.add_cascade(label="SERVO2", menu=menu_servo2_commands, font=FONT_MENU, underline=5)
        menu_mech_commands.add_cascade(label="SERVO3", menu=menu_servo3_commands, font=FONT_MENU, underline=5)
        menu_mech_commands.add_cascade(label="SERVO4", menu=menu_servo4_commands, font=FONT_MENU, underline=5)
        menu_mech_commands.add_cascade(label="EGG", menu=menu_egg_commands, font=FONT_MENU, underline=0)
        menu_mech_commands.add_cascade(label="RELEASE", menu=menu_release_commands, font=FONT_MENU, underline=0)
        menu_mech_commands.add_cascade(label="GUIDANCE", menu=menu_guidance_commands, font=FONT_MENU, underline=0)
        menu_mech_commands.add_cascade(label="CAM0", menu=menu_camera0_commands, font=FONT_MENU, underline=0)
        menu_mech_commands.add_cascade(label="CAM1", menu=menu_camera1_commands, font=FONT_MENU, underline=0)
        
        # Tack functions to those device menubar(s)
            # Servo 0
        menu_servo0_commands.add_command(label="0°", command=lambda:self._send_command("MEC,SERVO0,0"), font=FONT_MENU)
        menu_servo0_commands.add_command(label="30°", command=lambda:self._send_command("MEC,SERVO0,30"), font=FONT_MENU)
        menu_servo0_commands.add_command(label="45°", command=lambda:self._send_command("MEC,SERVO0,45"), font=FONT_MENU)
        menu_servo0_commands.add_command(label="60°", command=lambda:self._send_command("MEC,SERVO0,60"), font=FONT_MENU)
        menu_servo0_commands.add_command(label="90°", command=lambda:self._send_command("MEC,SERVO0,90"), font=FONT_MENU)
        menu_servo0_commands.add_command(label="180°", command=lambda:self._send_command("MEC,SERVO0,180"), font=FONT_MENU)
            # Servo 1
        menu_servo1_commands.add_command(label="0°", command=lambda:self._send_command("MEC,SERVO1,0"), font=FONT_MENU)
        menu_servo1_commands.add_command(label="30°", command=lambda:self._send_command("MEC,SERVO1,30"), font=FONT_MENU)
        menu_servo1_commands.add_command(label="45°", command=lambda:self._send_command("MEC,SERVO1,45"), font=FONT_MENU)
        menu_servo1_commands.add_command(label="60°", command=lambda:self._send_command("MEC,SERVO1,60"), font=FONT_MENU)
        menu_servo1_commands.add_command(label="90°", command=lambda:self._send_command("MEC,SERVO1,90"), font=FONT_MENU)
        menu_servo1_commands.add_command(label="180°", command=lambda:self._send_command("MEC,SERVO1,180"), font=FONT_MENU)
            # Servo 2
        menu_servo2_commands.add_command(label="0°", command=lambda:self._send_command("MEC,SERVO2,0"), font=FONT_MENU)
        menu_servo2_commands.add_command(label="30°", command=lambda:self._send_command("MEC,SERVO2,30"), font=FONT_MENU)
        menu_servo2_commands.add_command(label="45°", command=lambda:self._send_command("MEC,SERVO2,45"), font=FONT_MENU)
        menu_servo2_commands.add_command(label="60°", command=lambda:self._send_command("MEC,SERVO2,60"), font=FONT_MENU)
        menu_servo2_commands.add_command(label="90°", command=lambda:self._send_command("MEC,SERVO2,90"), font=FONT_MENU)
        menu_servo2_commands.add_command(label="180°", command=lambda:self._send_command("MEC,SERVO2,180"), font=FONT_MENU)
            # Servo 3
        menu_servo3_commands.add_command(label="0°", command=lambda:self._send_command("MEC,SERVO3,0"), font=FONT_MENU)
        menu_servo3_commands.add_command(label="30°", command=lambda:self._send_command("MEC,SERVO3,30"), font=FONT_MENU)
        menu_servo3_commands.add_command(label="45°", command=lambda:self._send_command("MEC,SERVO3,45"), font=FONT_MENU)
        menu_servo3_commands.add_command(label="60°", command=lambda:self._send_command("MEC,SERVO3,60"), font=FONT_MENU)
        menu_servo3_commands.add_command(label="90°", command=lambda:self._send_command("MEC,SERVO3,90"), font=FONT_MENU)
        menu_servo3_commands.add_command(label="180°", command=lambda:self._send_command("MEC,SERVO3,180"), font=FONT_MENU)
            # Servo 4
        menu_servo4_commands.add_command(label="0°", command=lambda:self._send_command("MEC,SERVO4,0"), font=FONT_MENU)
        menu_servo4_commands.add_command(label="30°", command=lambda:self._send_command("MEC,SERVO4,30"), font=FONT_MENU)
        menu_servo4_commands.add_command(label="45°", command=lambda:self._send_command("MEC,SERVO4,45"), font=FONT_MENU)
        menu_servo4_commands.add_command(label="60°", command=lambda:self._send_command("MEC,SERVO4,60"), font=FONT_MENU)
        menu_servo4_commands.add_command(label="90°", command=lambda:self._send_command("MEC,SERVO4,90"), font=FONT_MENU)
        menu_servo4_commands.add_command(label="180°", command=lambda:self._send_command("MEC,SERVO4,180"), font=FONT_MENU)
            # Egg
        menu_egg_commands.add_command(label="ON",command=lambda:self._send_command("MEC,EGG,ON"), font=FONT_MENU)
        menu_egg_commands.add_command(label="OFF",command=lambda:self._send_command("MEC,EGG,OFF"), font=FONT_MENU)
            # Release
        menu_release_commands.add_command(label="ON",command=lambda:self._send_command("MEC,RELEASE,ON"), font=FONT_MENU)
        menu_release_commands.add_command(label="OFF",command=lambda:self._send_command("MEC,RELEASE,OFF"), font=FONT_MENU)
            # Guidance
        menu_guidance_commands.add_command(label="LEFT",command=lambda:self._send_command("MEC,GUIDANCE,LEFT"), font=FONT_MENU)
        menu_guidance_commands.add_command(label="RIGHT",command=lambda:self._send_command("MEC,GUIDANCE,RIGHT"), font=FONT_MENU)
            # Camera 0
        menu_camera0_commands.add_command(label="ON",command=lambda:self._send_command("MEC,CAM0,ON"), font=FONT_MENU)
        menu_camera0_commands.add_command(label="OFF",command=lambda:self._send_command("MEC,CAM0,OFF"), font=FONT_MENU)
            # Camera 1
        menu_camera1_commands.add_command(label="ON",command=lambda:self._send_command("MEC,CAM1,ON"), font=FONT_MENU)
        menu_camera1_commands.add_command(label="OFF",command=lambda:self._send_command("MEC,CAM1,OFF"), font=FONT_MENU)
        
        # Create widgets (Master Widgets)
        label1 = tk.Label(self, text="Single Data Info [DEBUG]", background="red", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
        label2 = tk.Label(self, text="2D Graphs Field [DEBUG]", background="blue", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
        label3 = tk.Label(self, text="3D Graph and Confirm Field [DEBUG]", background="yellow", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
        label4 = tk.Label(self, text="Logos Field [DEBUG]", background="lime", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)

        # Scalar widgets (Mission Guide G8)
            # Larger Row Frames
        label_scalar_top = tk.Label(label1, text="Single Data Top [DEBUG]", background="pink", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
        label_scalar_bottom = tk.Label(label1, text="Single Data Bottom [DEBUG]", background="purple", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
            # TEAM_ID, MISSION_TIME, TEMPERATURE, GPS_POSITION, PACKET_RCV, PACKET_LOSS, FLIGHT_STATE, FLIGHT_MODE
                # Stubs
        label_stub_team_id = tk.Label(label_scalar_top, text="Team ID:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_mission_time = tk.Label(label_scalar_top, text="Mission Time:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_temperature = tk.Label(label_scalar_top, text="Temp (°C):", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_gps_pos = tk.Label(label_scalar_top, text="GPS (Lat/Long/Alt):", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_packet_rcv = tk.Label(label_scalar_bottom, text="Packets Received:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_packet_loss = tk.Label(label_scalar_bottom, text="Packets Lost:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_flight_state = tk.Label(label_scalar_bottom, text="Flight State:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_flight_mode = tk.Label(label_scalar_bottom, text="Flight Mode:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
                # Values
        label_team_id = tk.Label(label_scalar_top, text=str(self.latest_pkt.TEAM_ID), font=FONT_TEXT_BOLD, anchor="center")
        self.label_mission_time = tk.Label(label_scalar_top, text=self.latest_pkt.MISSION_TIME, font=FONT_TEXT_BOLD, anchor="center")
        self.label_temperature = tk.Label(label_scalar_top, text=self.latest_pkt.TEMPERATURE, font=FONT_TEXT_BOLD, anchor="center")
        self.label_gps_pos = tk.Label(label_scalar_top, text=f"{(float(self.latest_pkt.GPS_LATITUDE),float(self.latest_pkt.GPS_LONGITUDE),float(self.latest_pkt.GPS_ALTITUDE))}", font=FONT_TEXT_BOLD, anchor="center")
        self.label_packet_rcv = tk.Label(label_scalar_bottom, text=self.int_packet_rcv, font=FONT_TEXT_BOLD, anchor="center")
        self.label_packet_loss = tk.Label(label_scalar_bottom, text=self.int_packet_loss, font=FONT_TEXT_BOLD, anchor="center")
        self.label_flight_state = tk.Label(label_scalar_bottom, text=self.latest_pkt.STATE, font=FONT_TEXT_BOLD, anchor="center")
        self.label_flight_mode = tk.Label(label_scalar_bottom, text=self.latest_pkt.MODE, font=FONT_TEXT_BOLD, anchor="center")
            # Command Frame
        label_cmd_frame = tk.Label(label1, text="CMD FRAME [DEBUG]", font=FONT_TEXT_BOLD, bg=COLOR_BG_GRAY, anchor="center")
                # Command Frame Pieces
        label_stub_cmd = tk.Label(label_cmd_frame, text="CMD Input:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        self.label_cmd_entry = tk.Entry(label_cmd_frame, font=FONT_TEXT_BOLD, bg=COLOR_BG_GRAY, width=20)
        label_cmd_button = tk.Button(label_cmd_frame, text="Send", font=FONT_TITLE, bg=COLOR_BG_GRAY, command=self._cmd_button_callback)
        label_stub_echo = tk.Label(label_cmd_frame, text="CMD Echo:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        self.label_cmd_echo = tk.Entry(label_cmd_frame, font=FONT_TEXT_BOLD, bg=COLOR_BG_GRAY, width=20, state="readonly")
        
        # Bind the FocusIn callback to the entry field to remove the feedback messages I print in there
        self.label_cmd_entry.bind("<FocusIn>", self._cmd_entry_enter_callback)

        # Graph and Command Confirm widgets
        self.label_graph3D = tk.Label(label3, text="3D Graph Field [DEBUG]", background="orange", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
        label_stub_cmd_last = tk.Label(label3, text="Last Sent Command:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        self.label_cmd_last = tk.Label(label3, text=self.latest_sent_command, font=FONT_TEXT_BOLD, anchor="center")

        # Plot widgets (Mission Guide G7)
            # ALTITUDE, BATT_VOLTAGE, BATT_CURRENT, ACCELEROMETER(R,P,Y), ROTATION_RATES(R,P,Y)
        self.fig, self.axs = plt.subplots(3, 3, figsize=(20, 15), constrained_layout=True)  # 16 graphs in a 4x4 grid
        self.fig.patch.set_facecolor(COLOR_BG_GRAY)
        self.canvas = FigureCanvasTkAgg(self.fig, master=label2)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True) # Sets automatic resizing of the canvas
        self.str_plot_names = ["Altitude (m)", "Battery Voltage (V)", "Battery Current (A)", "Accel_R (deg/s²)", "Accel_P (deg/s²)", "Accel_Y (deg/s²)", "Gyro_R (deg/sec)", "Gyro_P (deg/sec)", "Gyro_Y (deg/sec)"]
        self.graphs_lines = list([None for i in range(0,3*3)])
        for i in range(0,3):
            for j in range(0,3):
                self.axs[i,j].set_title(self.str_plot_names[i*3+j], fontsize=14) # FIXME: Find a way to set the font to 14pt
                self.axs[i,j].tick_params(labelsize=14)

            # Create all the variables
        self.fig_3d = plt.figure()
        self.axs_3d = self.fig_3d.add_subplot(111, projection='3d') # Designates the axes as a 3d plot
        self.graph3d_line = None
        self.axs_3d.set_title('GPS Position', fontsize=14, fontweight='bold') # Plot title
        self.axs_3d.set_xlabel('Lat. (deg)', fontsize=14) # X-axis
        self.axs_3d.set_ylabel('Long. (deg)', fontsize=14) # Y-axis
        self.axs_3d.set_zlabel('Alt. (m)', fontsize=14) # Z-axis
        self.axs_3d.tick_params(labelsize=14)
        self.axs_3d.set_facecolor(COLOR_BG_GRAY)
        self.axs_3d.plot(self.gps_data[0], self.gps_data[1], self.gps_data[2], color='blue')
        self.axs_3d.view_init(azim=80)
        self.fig_3d.patch.set_facecolor(COLOR_BG_GRAY) # Light gray background
        self.canvas_3d = FigureCanvasTkAgg(self.fig_3d, master = self.label_graph3D)

        # Load UF gator logo image data and create widget for it
        imageFile_gators = Image.open("Images/Gators Logo.png")
        imageTk_gators = ImageTk.PhotoImage(imageFile_gators)
        label_gators_logo = tk.Label(label4, image=imageTk_gators, background=COLOR_BG_GRAY)

        # Load SSDC logo image data and create widget for it
        imageFile_ssdc = Image.open("Images/SSDC Logo Round.png")
        imageTk_ssdc = ImageTk.PhotoImage(imageFile_ssdc)
        label_ssdc_logo = tk.Label(label4, image=imageTk_ssdc, background=COLOR_BG_GRAY)

        # Define a resize function for the gator logo
        def eventFunc_imageTk_gators_resize(event):
            nonlocal imageTk_gators # Allow this function to modify the imageTk_gators variable
            imageFile_gators_rescale = imageFile_gators.copy() # Grab a copy of the image
            imageFile_gators_rescale.thumbnail((event.width, event.height), Image.LANCZOS) # Resize that copy to the size of the label using the LANCZOS resampling filter (there's no reason why that one was picked If there is a better one feel free to change it)
            imageTk_gators = ImageTk.PhotoImage(imageFile_gators_rescale) # Store that resized image into imageTk_gators
            label_gators_logo.config(image=imageTk_gators) # Refresh the image in tkinter to reflect the new image data

        # Define a resize function for the ssdc logo
        def eventFunc_imageTk_ssdc_resize(event):
            nonlocal imageTk_ssdc # Allow this function to modify the imageTk_ssdc variable
            imageFile_ssdc_rescale = imageFile_ssdc.copy() # Grab a copy of the image
            imageFile_ssdc_rescale.thumbnail((event.width, event.height), Image.LANCZOS) # Resize that copy to the size of the label using the LANCZOS resampling filter (there's no reason why that one was picked If there is a better one feel free to change it)
            imageTk_ssdc = ImageTk.PhotoImage(imageFile_ssdc_rescale) # Store that resized image into imageTk_ssdc
            label_ssdc_logo.config(image=imageTk_ssdc) # Refresh the image in tkinter to reflect the new image data

        # Bind the resize event functions to their labels
        label_gators_logo.bind("<Configure>", eventFunc_imageTk_gators_resize)
        label_ssdc_logo.bind("<Configure>", eventFunc_imageTk_ssdc_resize)

        # Configure the grid(s)
            # Root layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=3, uniform='a')
        self.columnconfigure(0, weight=6, uniform='a')
        self.columnconfigure(1, weight=2, uniform='a')
            # Label 1 (Scalar Widgets) Layout
        label1.rowconfigure(0, weight=2, uniform='a')
        label1.rowconfigure(1, weight=2, uniform='a')
        label1.rowconfigure(2, weight=1, uniform='a')
        label1.columnconfigure(0, weight=1, uniform='a')
            # Label 1 Top Row Layout
        label_scalar_top.rowconfigure(0, weight=1, uniform='a')
        label_scalar_top.rowconfigure(1, weight=1, uniform='a')
        label_scalar_top.columnconfigure(0, weight=1, uniform='a')
        label_scalar_top.columnconfigure(1, weight=1, uniform='a')
        label_scalar_top.columnconfigure(2, weight=1, uniform='a')
        label_scalar_top.columnconfigure(3, weight=2, uniform='a')
            # Label 1 Bottom Row Layout
        label_scalar_bottom.rowconfigure(0, weight=1, uniform='a')
        label_scalar_bottom.rowconfigure(1, weight=1, uniform='a')
        label_scalar_bottom.columnconfigure(0, weight=1, uniform='a')
        label_scalar_bottom.columnconfigure(1, weight=1, uniform='a')
        label_scalar_bottom.columnconfigure(2, weight=1, uniform='a')
        label_scalar_bottom.columnconfigure(3, weight=1, uniform='a')
            # Cmd Frame (Command Pieces) Layout
        label_cmd_frame.rowconfigure(0, weight=1, uniform='a')
        label_cmd_frame.columnconfigure(0, weight=1, uniform='a')
        label_cmd_frame.columnconfigure(1, weight=1, uniform='a')
        label_cmd_frame.columnconfigure(2, weight=1, uniform='a')
        label_cmd_frame.columnconfigure(3, weight=1, uniform='a')
        label_cmd_frame.columnconfigure(4, weight=1, uniform='a')
            # Label 3 (3d Graph and CMD Confirm field) Layout
        label3.rowconfigure(0, weight=7, uniform='a')
        label3.rowconfigure(1, weight=1, uniform='a')
        label3.rowconfigure(2, weight=1, uniform='a')
        label3.columnconfigure(0, weight=1, uniform='a')
            # Label 4 (Logos) Layout
        label4.rowconfigure(0, weight=1, uniform='a')
        label4.columnconfigure(0, weight=1, uniform='a')
        label4.columnconfigure(1, weight=1, uniform='a')

        # Attach the widgets to their grid positions
            # Root labels
        label1.grid(row = 0, column = 0, columnspan = 1, rowspan=1, sticky="nsew")
        label2.grid(row = 1, column = 0, columnspan = 1, rowspan=1, sticky="nsew")
        label3.grid(row = 1, column = 1, columnspan = 1, rowspan=1, sticky="nsew")
        label4.grid(row = 0, column = 1, columnspan = 1, rowspan=1, sticky="nsew")
            # Scalar Rows
        label_scalar_top.grid(row = 0, column = 0, sticky="nsew")
        label_scalar_bottom.grid(row = 1, column = 0, sticky="nsew")
            # Scalar Status labels
                # Stubs
        label_stub_team_id.grid(row = 0, column = 0, sticky="nsew")
        label_stub_mission_time.grid(row = 0, column = 1, sticky="nsew")
        label_stub_temperature.grid(row = 0, column = 2, sticky="nsew")
        label_stub_gps_pos.grid(row = 0, column = 3, columnspan = 2, sticky="nsew")
        label_stub_packet_rcv.grid(row = 0, column = 0, sticky="nsew")
        label_stub_packet_loss.grid(row = 0, column = 1, sticky="nsew")
        label_stub_flight_state.grid(row = 0, column = 2, sticky="nsew")
        label_stub_flight_mode.grid(row = 0, column = 3, sticky="nsew")
                # Values
        label_team_id.grid(row = 1, column = 0, sticky="nsew")
        self.label_mission_time.grid(row = 1, column = 1, sticky="nsew")
        self.label_temperature.grid(row = 1, column = 2, sticky="nsew")
        self.label_gps_pos.grid(row = 1, column = 3, sticky="nsew")
        self.label_packet_rcv.grid(row = 1, column = 0, sticky="nsew")
        self.label_packet_loss.grid(row = 1, column = 1, sticky="nsew")
        self.label_flight_state.grid(row = 1, column = 2, sticky="nsew")
        self.label_flight_mode.grid(row = 1, column = 3, sticky="nsew")
            # Command Frame
        label_cmd_frame.grid(row = 2, column = 0, sticky="nsew")
                # Command Frame Widgets
        label_stub_cmd.grid(row=0, column=0, sticky="nsew")
        self.label_cmd_entry.grid(row=0, column=1, sticky="nsew")
        label_cmd_button.grid(row=0, column=2, sticky="nsew")
        label_stub_echo.grid(row=0, column=3, sticky="nsew")
        self.label_cmd_echo.grid(row=0, column=4, sticky="nsew")
            # Logo labels
        label_gators_logo.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        label_ssdc_logo.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
            # Bottom Right Labels
        self.label_graph3D.grid(row = 0, column = 0, columnspan = 1, rowspan=1, sticky="nsew")
        self.canvas_3d.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True) # Sets automatic resizing of the canvas
                # Stubs
        label_stub_cmd_last.grid(row = 1, column = 0, columnspan = 1, rowspan=1, sticky="nsew")
                # Values
        self.label_cmd_last.grid(row = 2, column = 0, columnspan = 1, rowspan=1, sticky="nsew")


        #FIXME: Move the graph and 3d graph grid attachments down here

        # Set up the socket for packet retrieval
        self.sock_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_in.bind(ADDRESS_GUI)
        self.sock_in.listen(0)
        
        # Add socket to the tkinter event system
        self.tk.createfilehandler(self.sock_in, tk.READABLE | tk.WRITABLE, self._recv_msg_callback)

        # Finally we set the app icon on the way out
        imageFile_ssdc_icon = Image.open("Images/SSDC Icon.png")
        iconTk_ssdc = ImageTk.PhotoImage(imageFile_ssdc_icon)
        self.iconphoto(False, iconTk_ssdc)
        self.wm_iconphoto(True, iconTk_ssdc)

        return

    # Helper methods and callback functions

    def __del__(self):
        self.tk.deletefilehandler(self.sock_in)
        self.sock_in.close()
        self.sock_out.close()
        return

    def _menuFunc_exit(self):
        exit()
        return

    def _menuFunc_about(self): #TODO: Fill in text here with proper info
        messagebox.showinfo(
            "About This Application",
            "🚀Space Systems Design Club\nGround Control Station Application.\n\nVersion: 1.0\nAuthors: Phoenix Cushman & Anthony Torrell"
        )
        return

    def _menuFunc_burger(self):
        messagebox.showinfo(
            "Bon Appétit",
            "🍔"
        )
        return

    def _menuFunc_fries(self):
        messagebox.showinfo(
            "Bon Appétit",
            "🍟"
        )
        return

    def _menuFunc_dog(self):
        messagebox.showinfo(
            "Bon Appétit",
            "🌭"
        )
        return


    def _cmd_entry_enter_callback(self, event):

        self.label_cmd_entry.config(fg="black")

        if self.int_cmd_entry_state == 1:
            self.int_cmd_entry_state = 0
            self.label_cmd_entry.delete(0, tk.END)
        return

    def _cmd_button_callback(self):

        self.focus_force()

        cmd_str = self.label_cmd_entry.get()
        fields = cmd_str.split(',')
        cmd_field = fields[0]
        self.label_cmd_entry.delete(0, tk.END)

        if self.int_cmd_entry_state == 1:
            self.int_cmd_entry_state = 0
            self.label_cmd_entry.delete(0, tk.END)
            self.label_cmd_entry.config(fg="black")
        else:
            match(cmd_field):
                case "CX_ON":
                    self._send_command("CX_ON")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "CX_OFF":
                    self._send_command("CX_OFF")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "ST_UTC":
                    self._send_command("ST_UTC")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "ST_GPS":
                    self._send_command("ST_GPS")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "SIM_EN":
                    self._send_command("SIM_EN")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "SIM_ACT":
                    self._send_command("SIM_ACT")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "SIM_DIS":
                    self._send_command("SIM_DIS")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "CAL":
                    self._send_command("CAL")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "MEC":
                    if len(fields) >= 3:
                        self._send_command(f"{cmd_str}")
                        self.int_cmd_entry_state = 1
                        self.label_cmd_entry.config(fg="green")
                        self.label_cmd_entry.insert(0, "COMMAND SENT")
                    else:
                        self.int_cmd_entry_state = 1
                        self.label_cmd_entry.config(fg="red")
                        self.label_cmd_entry.insert(0, "INVALID COMMAND")
                case "GNC_ACT":
                    self._send_command("GNC_ACT")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case _:
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="red")
                    self.label_cmd_entry.insert(0, "INVALID COMMAND")
                
        return

    # This callback function currently only reads one packet before closing the client connection so the client has to re-connect for every packet sent
    def _recv_msg_callback(self, sock, mask):
        
        # Set up the client connection
        client_socket, client_address = sock.accept()
        #print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        # Read in a message from the client
        msg = client_socket.recv(1024)
        msg = msg.decode("utf-8") # convert bytes to string

        # Close the connection
        client_socket.close()

        # Print the msg to the terminal and start parsing it with the TelemetryPacket class
        #print(f"[DEBUG] GUI Recv: {msg}\n")
        pkt = telemetryPacket.TelemetryPacket(msg)

        if pkt.TEAM_ID != self.TEAM_ID:
            print(f"Someone Else's Packet Received: {msg}\n")
        else:
            self.latest_pkt = pkt
            self._update_all()

        return

    def _update_all(self):
        # Process the new data
        #   TEAM_ID, MISSION_TIME, PACKET_COUNT, MODE, STATE, ALTITUDE,
        #   TEMPERATURE, PRESSURE, VOLTAGE, CURRENT, GYRO_R, GYRO_P,
        #   GYRO_Y, ACCEL_R, ACCEL_P, ACCEL_Y, GPS_TIME, GPS_ALTITUDE,
        #   GPS_LATITUDE, GPS_LONGITUDE, GPS_SATS, CMD_ECHO [,,OPTIONAL_DATA]

        # Mission Time
        self.label_mission_time.config(text=self.latest_pkt.MISSION_TIME)

        # Packet Count
        self.int_packet_rcv += 1
        self.label_packet_rcv.config(text=self.int_packet_rcv)
        self.int_packet_loss = int(self.latest_pkt.PACKET_COUNT) - self.int_packet_rcv
        self.label_packet_loss.config(text=self.int_packet_loss)

        # Flight Mode
        self.label_flight_mode.config(text=self.latest_pkt.MODE)

        # Flight State
        self.label_flight_state.config(text=self.latest_pkt.STATE)

        # Temperature
        self.label_temperature.config(text=self.latest_pkt.TEMPERATURE)

        # Voltage, Current, Gyro (RPY), Altitude (RPY)
        self._insert_graph_data(
            list([float(self.latest_pkt.ALTITUDE),
            float(self.latest_pkt.VOLTAGE),
            float(self.latest_pkt.CURRENT),
            float(self.latest_pkt.ACCEL_R),
            float(self.latest_pkt.ACCEL_P),
            float(self.latest_pkt.ACCEL_Y),
            float(self.latest_pkt.GYRO_R),
            float(self.latest_pkt.GYRO_P),
            float(self.latest_pkt.GYRO_Y)])
        )
        self._update_graphs_callback()

        # GPS Location
        # FIXME: Put this back once we have good data to read
        self.label_gps_pos.config(text=f"{(float(self.latest_pkt.GPS_LATITUDE),float(self.latest_pkt.GPS_LONGITUDE),float(self.latest_pkt.GPS_ALTITUDE))}")
        self._insert_gps_data([float(self.latest_pkt.GPS_LATITUDE),float(self.latest_pkt.GPS_LONGITUDE),float(self.latest_pkt.GPS_ALTITUDE)])

        # Command Echo
        self.label_cmd_echo.config(state="normal")
        self.label_cmd_echo.delete(0, tk.END)
        self.label_cmd_echo.insert(0, self.latest_pkt.CMD_ECHO)
        self.label_cmd_echo.config(state="readonly")

        return

    def _insert_graph_data(self, arr):
        # Advance the packet number along the x axis of all the graphs
        if len(self.graph_domain) == 0:
            self.graph_domain = [1]
        else:
            self.graph_domain += [int(self.latest_pkt.PACKET_COUNT)]
        # Truncate the old values after it gets to a length of 10
        if len(self.graph_domain) > 10:
            self.graph_domain = self.graph_domain[1:]

        # Insert the new graph data
        for i in range(0,9):
            self.graph_data[i] += [arr[i]]
            # Truncate the old values after it gets to a length of 10
            if len(self.graph_data[i]) > 10:
                self.graph_data[i] = self.graph_data[i][1:]
        return
    
    def _insert_gps_data(self, arr):
        for i in range(0,3):
            self.gps_data[i] += [arr[i]]
            if len(self.gps_data[i]) > 10:
                self.gps_data[i] = self.gps_data[i][1:]
        return

    def _update_graphs_callback(self):
        for i in range(0,3):
            for j in range(0,3):
                if (self.graphs_lines[i*3+j] == None):
                    self.graphs_lines[i*3+j], = self.axs[i,j].plot(self.graph_data[i*3+j])
                else:
                    self.graphs_lines[i*3+j].set_data(self.graph_domain, self.graph_data[i*3+j])
                    self.axs[i,j].tick_params(labelsize=14)
                    self.axs[i,j].relim()
                    self.axs[i,j].autoscale_view()
        if (self.graph3d_line == None):
            self.graph3d_line, = self.axs_3d.plot(self.gps_data[0], self.gps_data[1], self.gps_data[2], color=COLOR_GATOR_BLUE)
        else:
            #self.graph3d_line.set_data_3d(self.gps_data[0], self.gps_data[1], self.gps_data[2])
            self.graph3d_line.remove()
            self.graph3d_line, = self.axs_3d.plot(self.gps_data[0], self.gps_data[1], self.gps_data[2], color=COLOR_GATOR_BLUE)
            self.axs_3d.set_xlim(min(self.gps_data[0])-10, max(self.gps_data[0])+10)
            self.axs_3d.set_ylim(min(self.gps_data[1])-10, max(self.gps_data[1])+10)
            self.axs_3d.set_zlim(min(self.gps_data[2])-10, max(self.gps_data[2])+10)
            self.axs_3d.autoscale_view(tight=True, scalex=True, scaley=True, scalez=True)
        #FIXME: Put back
        self.canvas.draw()
        self.canvas_3d.draw()
        plt.draw()
        return

    def demo_graph_print(self):
        print("[DEBUG] Demo Callback")
        self._insert_graph_data(
            [random.randint(1,5),
            random.randint(1,5),
            random.randint(1,5),
            random.randint(1,5),
            random.randint(1,5),
            random.randint(1,5),
            random.randint(1,5),
            random.randint(1,5),
            random.randint(1,5)]
        )
        self._update_graphs_callback()
        self.after(1000, self.demo_graph_print)
        return

    # GCS to Flight Software Commands
    def _send_command(self,cmd):
        
        # First send some data
        msg = cmd
        sock_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_out.connect(ADDRESS_TH)
        sock_out.send(msg.encode('utf-8'))
        sock_out.close()
        
        print("[DEBUG] GUI Sent:", msg)

        self.latest_sent_command = msg
        # ALL NON-FSW COMMANDS MUST START WITH AN ASTERISK TO PREVENT PRINTING
        if msg[0] != '*':
            self.label_cmd_last.config(text=self.latest_sent_command)

        return

    def _menuFunc_reset_3d(self):
        self.axs_3d.view_init(azim=80)
        plt.draw()
        return