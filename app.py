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

########################## Global Variables ##########################

# Colors and Fonts for Blue and Orange Theme
global COLOR_BG_GRAY;           COLOR_BG_GRAY = '#F0F0F0'               # Light gray
#global COLOR_BG_CREAM;           COLOR_BG_CREAM = '#FFF7F0'               # Light Orange
global COLOR_GATOR_ORANGE;      COLOR_GATOR_ORANGE = "#FA4616"          # Gator Orange
global COLOR_GATOR_BLUE;        COLOR_GATOR_BLUE = "#0021A5"            # Gator Blue
global COLOR_GATOR_GREEN;       COLOR_GATOR_GREEN = "#22884C"           # Gator Green
global COLOR_SSDC_NAVY;         COLOR_SSDC_NAVY = "#001F3C"             # SSDC Navy Blue
global COLOR_FADED_TEXT;        COLOR_FADED_TEXT = "#929292"            # Mute gray
#global FONT_TITLE;              FONT_TITLE = ("Comic Sans MS", 16, "bold")
#global FONT_TITLE;              FONT_TITLE = ("Nexa Round_Trial Glow", 16, "bold")
global FONT_TITLE;              FONT_TITLE = ("Verdana", 16, "bold")
global FONT_MENU;               FONT_MENU = ("Verdana", 14, "bold")
global FONT_TEXT_BOLD;          FONT_TEXT_BOLD = ("Verdana", 14, "bold")
global FONT_TEXT_BOLD_UNDER;    FONT_TEXT_BOLD_UNDER = ("Verdana", 14, "bold", "underline")
global FONT_DEBUG;              FONT_DEBUG = ("Verdana", 16, "bold")

# Mission Info Variables
global TEAM_ID;                 TEAM_ID = "1075"

######################################################################

class App(tk.Tk):
  
    # Make all the readout variables
    str_team_id = f"{TEAM_ID}"
    str_mission_time = f"{'--:--:--'}"
    str_temperature = f"{'WARM'}"
    tup_gps_pos = (1,1,1)
    str_gps_pos = f"{tup_gps_pos}"
    int_packet_rcv = 0
    str_packet_rcv = f"{int_packet_rcv}"
    int_packet_loss = 0
    str_packet_loss = f"{int_packet_loss}"
    str_flight_state = f"{'F(LORIDA)'}"
    str_flight_mode = f"{'DANCE'}"
    str_cmd_echo = ""
    int_cmd_entry_state = 0

    graphdata = [
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

    def __init__(self):
        # Create the main window
        super().__init__()

        # Add the color and size properties to the main window
        self.title("Tkinter Grid Testing Python Cansat 2025-2026")
        self.configure(bg=COLOR_BG_GRAY)
        width = self.winfo_screenwidth() # Gets the screen dimensions
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height)) # Sets the dimensions of the window to those screen dimensions

        # Linux Version of Zoom
        self.state('zoomed')

        # Create the main menubar and assign as the root's menu
        menubar = tk.Menu(self)
        self.config(menu=menubar) # Attach the menubar to the root window

        # Create menu bar objects
        menu_file = tk.Menu(menubar, tearoff=False)
        menu_food = tk.Menu(menubar, tearoff=False)
        menu_commands = tk.Menu(menubar, tearoff=False)
        menu_help = tk.Menu(menubar, tearoff=False)

        # Create tabs from those objects
        menubar.add_cascade(label="File", menu=menu_file, font=FONT_MENU)
        menubar.add_cascade(label="Food", menu=menu_food, font=FONT_MENU)
        menubar.add_cascade(label="CMD", menu=menu_commands, font=FONT_MENU)
        menubar.add_cascade(label="Help", menu=menu_help, font=FONT_MENU)

        # Tack functions to those tabs 
        menu_file.add_command(label="Exit", command=self.menuFunc_exit, font=FONT_MENU)
        menu_help.add_command(label="About", command=self.menuFunc_about, font=FONT_MENU)
        menu_food.add_command(label="Burger", command=self.menuFunc_burger, font=FONT_MENU)
        menu_food.add_command(label="Fries", command=self.menuFunc_fries, font=FONT_MENU)

        # Create widgets
        label1 = tk.Label(self, text="Single Data Info [DEBUG]", background="red", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
        label2 = tk.Label(self, text="2D Graphs Field [DEBUG]", background="blue", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
        label3 = tk.Label(self, text="3D Graph Field [DEBUG]", background="yellow", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
        label4 = tk.Label(self, text="Logos Field [DEBUG]", background="lime", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)

        # Scalar widgets (Mission Guide G8)
            # TEAM_ID, MISSION_TIME, TEMPERATURE, GPS_POSITION, PACKET_RCV, PACKET_LOSS, FLIGHT_STATE, FLIGHT_MODE
                # Stubs
        label_stub_team_id = tk.Label(label1, text="Team ID:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_mission_time = tk.Label(label1, text="Mission Time:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_temperature = tk.Label(label1, text="Temp:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_gps_pos = tk.Label(label1, text="GPS:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_packet_rcv = tk.Label(label1, text="Packets Received:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_packet_loss = tk.Label(label1, text="Packets Lost:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_flight_state = tk.Label(label1, text="Flight State:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_flight_mode = tk.Label(label1, text="Flight Mode:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
                # Values
        label_team_id = tk.Label(label1, text=str(self.str_team_id), font=FONT_TEXT_BOLD, anchor="center")
        self.label_mission_time = tk.Label(label1, text=self.str_mission_time, font=FONT_TEXT_BOLD, anchor="center")
        label_temperature = tk.Label(label1, text=self.str_temperature, font=FONT_TEXT_BOLD, anchor="center")
        label_gps_pos = tk.Label(label1, text=self.str_gps_pos, font=FONT_TEXT_BOLD, anchor="center")
        self.label_packet_rcv = tk.Label(label1, text=self.str_packet_rcv, font=FONT_TEXT_BOLD, anchor="center")
        self.label_packet_loss = tk.Label(label1, text=self.str_packet_loss, font=FONT_TEXT_BOLD, anchor="center")
        label_flight_state = tk.Label(label1, text=self.str_flight_state, font=FONT_TEXT_BOLD, anchor="center")
        label_flight_mode = tk.Label(label1, text=self.str_flight_mode, font=FONT_TEXT_BOLD, anchor="center")
                # Command Frame Pieces
        label_cmd_frame = tk.Label(label1, text="CMD FRAME [DEBUG]", font=FONT_TEXT_BOLD, bg=COLOR_BG_GRAY, anchor="center")
        label_stub_cmd = tk.Label(label_cmd_frame, text="Command Input:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        self.label_cmd_entry = tk.Entry(label_cmd_frame, font=FONT_TEXT_BOLD, bg=COLOR_BG_GRAY, width=20)
        label_cmd_button = tk.Button(label_cmd_frame, text="Send", font=FONT_TITLE, bg=COLOR_BG_GRAY, command=self.cmd_button_callback)
        label_stub_echo = tk.Label(label_cmd_frame, text="Command Echo:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, bg=COLOR_BG_GRAY, anchor="center")
        self.label_cmd_echo = tk.Entry(label_cmd_frame, font=FONT_TEXT_BOLD, bg=COLOR_BG_GRAY, width=20, state="disabled")
        
        # Bind the FocusIn callback to the entry field to remove the feedback messages I print in their
        self.label_cmd_entry.bind("<FocusIn>", self.cmd_entry_enter_callback)

        # Plot widgets (Mission Guide G7)
            # ALTITUDE, BATT_VOLTAGE, BATT_CURRENT, ACCELEROMETER(R,P,Y), ROTATION_RATES(R,P,Y)
        self.fig, self.axs = plt.subplots(3, 3, figsize=(20, 15), constrained_layout=True)  # 16 graphs in a 4x4 grid
        self.fig.patch.set_facecolor(COLOR_BG_GRAY)
        self.canvas = FigureCanvasTkAgg(self.fig, master=label2)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True) # Sets automatic resizing of the canvas

        self.str_plot_names = ["Altitude", "Battery Voltage", "Battery Current", "Accel_R", "Accel_P", "Accel_Y", "Gyro_R", "Gyro_P", "Gyro_Y"]
        for i in range(0,3):
            for j in range(0,3):
                self.axs[i,j].set_title(self.str_plot_names[i*3+j])
        #self.update_graphs_callback()
        

        # Load UF gator logo image data and create widget for it
        imageFile_gators = Image.open("Images/Gators Logo.png")
        imageTk_gators = ImageTk.PhotoImage(imageFile_gators)
        label_gators_logo = tk.Label(label4, image=imageTk_gators, background=COLOR_GATOR_GREEN)

        # Load SSDC logo image data and create widget for it
        imageFile_ssdc = Image.open("Images/SSDC Logo green.png")
        imageTk_ssdc = ImageTk.PhotoImage(imageFile_ssdc)
        label_ssdc_logo = tk.Label(label4, image=imageTk_ssdc, background=COLOR_GATOR_GREEN)

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
        label1.rowconfigure(0, weight=1, uniform='a')
        label1.rowconfigure(1, weight=1, uniform='a')
        label1.rowconfigure(2, weight=1, uniform='a')
        label1.rowconfigure(3, weight=1, uniform='a')
        label1.rowconfigure(4, weight=1, uniform='a')
        label1.columnconfigure(0, weight=1, uniform='a')
        label1.columnconfigure(1, weight=1, uniform='a')
        label1.columnconfigure(2, weight=1, uniform='a')
        label1.columnconfigure(3, weight=1, uniform='a')
            # Cmd Frame (Command Pieces) Layout
        label_cmd_frame.rowconfigure(0, weight=1, uniform='a')
        label_cmd_frame.columnconfigure(0, weight=1, uniform='a')
        label_cmd_frame.columnconfigure(1, weight=1, uniform='a')
        label_cmd_frame.columnconfigure(2, weight=1, uniform='a')
        label_cmd_frame.columnconfigure(3, weight=1, uniform='a')
        label_cmd_frame.columnconfigure(4, weight=1, uniform='a')
            # Label 4 (Logos) Layout
        label4.rowconfigure(0, weight=1, uniform='a')
        label4.columnconfigure(0, weight=1, uniform='a')
        label4.columnconfigure(1, weight=1, uniform='a')

        # Attach the widgets to their grid positions
            # Root labels
        label1.grid(row = 0, column = 0, columnspan = 1, rowspan=1, sticky="nsew")
        label2.grid(row = 1, column = 0, columnspan = 2, rowspan=1, sticky="nsew")
        #label3.grid(row = 1, column = 1, columnspan = 1, rowspan=1, sticky="nsew")
        label4.grid(row = 0, column = 1, columnspan = 1, rowspan=1, sticky="nsew")
            # Scalar Status labels
                # Stubs
        label_stub_team_id.grid(row = 0, column = 0, sticky="nsew")
        label_stub_mission_time.grid(row = 0, column = 1, sticky="nsew")
        label_stub_temperature.grid(row = 0, column = 2, sticky="nsew")
        label_stub_gps_pos.grid(row = 0, column = 3, sticky="nsew")
        label_stub_packet_rcv.grid(row = 2, column = 0, sticky="nsew")
        label_stub_packet_loss.grid(row = 2, column = 1, sticky="nsew")
        label_stub_flight_state.grid(row = 2, column = 2, sticky="nsew")
        label_stub_flight_mode.grid(row = 2, column = 3, sticky="nsew")
                # Values
        label_team_id.grid(row = 1, column = 0, sticky="nsew")
        self.label_mission_time.grid(row = 1, column = 1, sticky="nsew")
        label_temperature.grid(row = 1, column = 2, sticky="nsew")
        label_gps_pos.grid(row = 1, column = 3, sticky="nsew")
        self.label_packet_rcv.grid(row = 3, column = 0, sticky="nsew")
        self.label_packet_loss.grid(row = 3, column = 1, sticky="nsew")
        label_flight_state.grid(row = 3, column = 2, sticky="nsew")
        label_flight_mode.grid(row = 3, column = 3, sticky="nsew")
                # Command Frame
        label_cmd_frame.grid(row = 4, column = 0, columnspan = 4, sticky="nsew")
        label_stub_cmd.grid(row=0, column=0, sticky="nsew")
        self.label_cmd_entry.grid(row=0, column=1, sticky="nsew")
        label_cmd_button.grid(row=0, column=2, sticky="nsew")
        label_stub_echo.grid(row=0, column=3, sticky="nsew")
        self.label_cmd_echo.grid(row=0, column=4, sticky="nsew")
            # Logo labels
        label_gators_logo.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        label_ssdc_logo.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

        # Finally we set the app icon on the way out
        imageFile_ssdc_icon = Image.open("Images/SSDC Icon.png")
        iconTk_ssdc = ImageTk.PhotoImage(imageFile_ssdc_icon)
        self.iconphoto(False, iconTk_ssdc)

        return

    def __del__(self):
        self.tk.deletefilehandler(self.sock)
        self.sock.close()

    def menuFunc_exit(self):
        exit()

    def menuFunc_about(self): #TODO: Fill in text here with proper info
        messagebox.showinfo(
            "About This Application",
            "This is a sample Tkinter application.\n\nVersion: 1.0\nAuthor: CANSAT"
        )
        return

    def menuFunc_burger(self):
        messagebox.showinfo(
            "Bon Appétit",
            "🍔"
        )

    def menuFunc_fries(self):
        messagebox.showinfo(
            "Bon Appétit",
            "🍟"
        )

    def cmd_button_callback(self):

        self.focus_force()

        cmd_str = self.label_cmd_entry.get()
        self.label_cmd_entry.delete(0, tk.END)

        if self.int_cmd_entry_state == 1:
            self.int_cmd_entry_state = 0
            self.label_cmd_entry.delete(0, tk.END)
            self.label_cmd_entry.config(fg="black")
        else:
            match(cmd_str):
                case "CXON":
                    print(f"[DEBUG] Command Sent: {cmd_str}")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "CXOFF":
                    print(f"[DEBUG] Command Sent: {cmd_str}")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "ST":
                    print(f"[DEBUG] Command Sent: {cmd_str}")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "SIM":
                    print(f"[DEBUG] Command Sent: {cmd_str}")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "SIMP":
                    print(f"[DEBUG] Command Sent: {cmd_str}")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "CAL":
                    print(f"[DEBUG] Command Sent: {cmd_str}")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case "MEC":
                    print(f"[DEBUG] Command Sent: {cmd_str}")
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="green")
                    self.label_cmd_entry.insert(0, "COMMAND SENT")
                case _:
                    self.int_cmd_entry_state = 1
                    self.label_cmd_entry.config(fg="red")
                    self.label_cmd_entry.insert(0, "INVALID COMMAND")
                
        return

    def cmd_entry_enter_callback(self, event):

        self.label_cmd_entry.config(fg="black")

        if self.int_cmd_entry_state == 1:
            self.int_cmd_entry_state = 0
            self.label_cmd_entry.delete(0, tk.END)

