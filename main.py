# Libraries and Packages
import tkinter as tk
from tkinter import messagebox

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1) # Make the application DPI aware

from PIL import Image, ImageTk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


########################## Global Variables ##########################

# Colors and Fonts for Blue and Orange Theme
global COLOR_BG_GRAY;           COLOR_BG_GRAY = '#F0F0F0'               # Light gray
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
global TEAM_ID;                 TEAM_ID = "TBD"

######################################################################

def main():
    print("*********************************")
    print("*  Tkinter Grid Testing Python  *")
    print("*      Cansat 2025-2026         *")
    print("*********************************")

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

    # Create the main window
    root = tk.Tk()

    # Add the color and size properties to the main window
    root.title("Tkinter Grid Testing Python Cansat 2025-2026")
    root.configure(bg=COLOR_BG_GRAY)
    width = root.winfo_screenwidth() # Gets the screen dimensions
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height)) # Sets the dimensions of the window to those screen dimensions
    root.state('zoomed') # Automatically maximizes the Window

    # Create the main menubar and assign as the root's menu
    menubar = tk.Menu(root)
    root.config(menu=menubar) # Attach the menubar to the root window

    # Create menu bar objects
    menu_file = tk.Menu(menubar, tearoff=False)
    menu_food = tk.Menu(menubar, tearoff=False)
    menu_help = tk.Menu(menubar, tearoff=False)

    # Create tabs from those objects
    menubar.add_cascade(label="File", menu=menu_file, font=FONT_MENU)
    menubar.add_cascade(label="Food", menu=menu_food, font=FONT_MENU)
    menubar.add_cascade(label="Help", menu=menu_help, font=FONT_MENU)

    # Tack functions to those tabs 
    menu_file.add_command(label="Exit", command=menuFunc_exit, font=FONT_MENU)
    menu_help.add_command(label="About", command=menuFunc_about, font=FONT_MENU)
    menu_food.add_command(label="Burger", command=menuFunc_burger, font=FONT_MENU)
    menu_food.add_command(label="Fries", command=menuFunc_fries, font=FONT_MENU)

    # Create widgets
    label1 = tk.Label(root, text="Single Data Info [DEBUG]", background="red", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
    label2 = tk.Label(root, text="2D Graphs Field [DEBUG]", background="blue", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
    label3 = tk.Label(root, text="3D Graph Field [DEBUG]", background="yellow", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)
    label4 = tk.Label(root, text="Logos Field [DEBUG]", background="lime", font=FONT_DEBUG, highlightthickness=0, borderwidth=0)

    # Scalar widgets (Mission Guide G8)
        # TEAM_ID, MISSION_TIME, TEMPERATURE, GPS_POSITION, PACKET_RCV, PACKET_LOSS, FLIGHT_SOFTWARE_STATE
            # Stubs
    label_stub_team_id = tk.Label(label1, text="Team ID:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, anchor="center")
    label_stub_mission_time = tk.Label(label1, text="Mission Time:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, anchor="center")
    label_stub_temperature = tk.Label(label1, text="Temp:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, anchor="center")
    label_stub_gps_pos = tk.Label(label1, text="GPS:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, anchor="center")
    label_stub_packet_rcv = tk.Label(label1, text="Packets Received:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, anchor="center")
    label_stub_packet_loss = tk.Label(label1, text="Packets Lost:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, anchor="center")
    label_stub_flight_state = tk.Label(label1, text="Flight Software State:", font=FONT_TEXT_BOLD_UNDER, fg=COLOR_FADED_TEXT, anchor="center")
            # Values
    label_team_id = tk.Label(label1, text=str(str_team_id), font=FONT_TEXT_BOLD, anchor="center")
    label_mission_time = tk.Label(label1, text=str_mission_time, font=FONT_TEXT_BOLD, anchor="center")
    label_temperature = tk.Label(label1, text=str_temperature, font=FONT_TEXT_BOLD, anchor="center")
    label_gps_pos = tk.Label(label1, text=str_gps_pos, font=FONT_TEXT_BOLD, anchor="center")
    label_packet_rcv = tk.Label(label1, text=str_packet_rcv, font=FONT_TEXT_BOLD, anchor="center")
    label_packet_loss = tk.Label(label1, text=str_packet_loss, font=FONT_TEXT_BOLD, anchor="center")
    label_flight_state = tk.Label(label1, text=str_flight_state, font=FONT_TEXT_BOLD, anchor="center")
            # Command Frame
    label_cmd_frame = tk.Label(label1, text="CMD FRAME [DEBUG]", font=FONT_DEBUG, fg=COLOR_GATOR_ORANGE, anchor="center")
    #label_cmd_echo = tk.Label(label1, text=f"Command Echo: {'---'}", font=FONT_TITLE, anchor="center") #This will go into the command frame later

    # Plot widgets (Mission Guide G7)
        # ALTITUDE, BATT_VOLTAGE, BATT_CURRENT, ACCELEROMETER, ROTATION_RATES
    # FUTURE WIDGETS GO HERE
    

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
    root.rowconfigure(0, weight=1, uniform='a')
    root.rowconfigure(1, weight=3, uniform='a')
    root.columnconfigure(0, weight=6, uniform='a')
    root.columnconfigure(1, weight=2, uniform='a')
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
        # Scalar Status labels
            # Stubs
    label_stub_team_id.grid(row = 0, column = 0, sticky="nsew")
    label_stub_mission_time.grid(row = 0, column = 1, sticky="nsew")
    label_stub_temperature.grid(row = 0, column = 2, sticky="nsew")
    label_stub_gps_pos.grid(row = 0, column = 3, sticky="nsew")
    label_stub_packet_rcv.grid(row = 2, column = 0, sticky="nsew")
    label_stub_packet_loss.grid(row = 2, column = 1, sticky="nsew")
    label_stub_flight_state.grid(row = 2, column = 2, columnspan = 2, sticky="nsew")
            # Values
    label_team_id.grid(row = 1, column = 0, sticky="nsew")
    label_mission_time.grid(row = 1, column = 1, sticky="nsew")
    label_temperature.grid(row = 1, column = 2, sticky="nsew")
    label_gps_pos.grid(row = 1, column = 3, sticky="nsew")
    label_packet_rcv.grid(row = 3, column = 0, sticky="nsew")
    label_packet_loss.grid(row = 3, column = 1, sticky="nsew")
    label_flight_state.grid(row = 3, column = 2, columnspan = 2, sticky="nsew")
            # Command Frame
    label_cmd_frame.grid(row = 4, column = 0, columnspan = 4, sticky="nsew")
    #label_cmd_echo.grid(row = 2, column = 2, columnspan = 2, sticky="nsew") #This will go into the command frame later
        # Logo labels
    label_gators_logo.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    label_ssdc_logo.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    ###########################################################################################
    # TEST CODE IN HERE
    ###########################
    #

    '''

    root2 = tk.Tk()

    root2.rowconfigure(0, weight=1, uniform='a')
    root2.columnconfigure(0, weight=1, uniform='a')

    '' '
    def send_command():
        #nonlocal CMD_ECHO
        nonlocal cmd_echo_label
        #CMD_ECHO = cmd_entry.get()
        #print(f"[DEBUG] Send Command Function go! '{CMD_ECHO}'")
        print(f"[DEBUG] Send Command Function go! '{cmd_entry.get()}'")
        #cmd_echo_label.config(text=f"Command Echo: {CMD_ECHO}")
        cmd_echo_label.config(text=f"Command Echo: {commandEcho(cmd_entry.get())}")
    '' '

    # Make the master label
    master_temp_label = tk.Label(root2, text="testing :3", font=FONT_TITLE, background=COLOR_GATOR_GREEN, highlightthickness=0, borderwidth=0)

    # Make all the readout widgets

    # Make all the readout variables
    str_team_id = f"Team ID: {TEAM_ID}"
    str_mission_time = f"Mission Time: {'--:--:--'}"
    str_temperature = f"Temp: {'WARM'}"
    tup_gps_pos = (1,1,1)
    str_gps_pos = f"GPS: {tup_gps_pos}"
    int_packet_rcv = 0
    str_packet_rcv = f"Packets Received: {int_packet_rcv}"
    int_packet_loss = 0
    str_packet_loss = f"Packets Lost: {int_packet_loss}"
    str_flight_state = f"Flight Software State: {'F(LORIDA)'}"


    # Scalar widgets (Mission Guide G8)
        # TEAM_ID, MISSION_TIME, TEMPERATURE, GPS_POSITION, PACKET_RCV, PACKET_LOSS, FLIGHT_SOFTWARE_STATE
    label_team_id = tk.Label(master_temp_label, text=str_team_id, font=FONT_TITLE, anchor="w")
    label_mission_time = tk.Label(master_temp_label, text=str_mission_time, font=FONT_TITLE, anchor="w")
    label_temperature = tk.Label(master_temp_label, text=str_temperature, font=FONT_TITLE, anchor="e")
    label_gps_pos = tk.Label(master_temp_label, text=str_gps_pos, font=FONT_TITLE, anchor="e")
    label_packet_rcv = tk.Label(master_temp_label, text=str_packet_rcv, font=FONT_TITLE, anchor="w")
    label_packet_loss = tk.Label(master_temp_label, text=str_packet_loss, font=FONT_TITLE, anchor="w")
    label_flight_state = tk.Label(master_temp_label, text=str_flight_state, font=FONT_TITLE, anchor="e")
    label_cmd_frame = tk.Label(master_temp_label, text="CMD FRAME [DEBUG]", font=FONT_TITLE, anchor="center")


    # Plot widgets (Mission Guide G7)
        # ALTITUDE, BATT_VOLTAGE, BATT_CURRENT, ACCELEROMETER, ROTATION_RATES




    #cmd_echo_label = tk.Label(cmd_frame, text=f"Command Echo: {'---'}", font=FONT_TITLE, bg="#FF6060", fg=COLOR_GATOR_ORANGE)

    # Build a 4x3 Grid
    master_temp_label.rowconfigure(0, weight=1, uniform='a')
    master_temp_label.rowconfigure(1, weight=1, uniform='a')
    master_temp_label.rowconfigure(2, weight=1, uniform='a')
    master_temp_label.columnconfigure(0, weight=1, uniform='a')
    master_temp_label.columnconfigure(1, weight=1, uniform='a')
    master_temp_label.columnconfigure(2, weight=1, uniform='a')
    master_temp_label.columnconfigure(3, weight=1, uniform='a')



    # Attach all the widgets
    master_temp_label.grid(row = 0, column = 0, columnspan = 1, rowspan=1, sticky="nsew")
    label_team_id.grid(row = 0, column = 0, sticky="nsew")
    label_mission_time.grid(row = 0, column = 1, sticky="nsew")
    label_temperature.grid(row = 0, column = 2, sticky="nsew")
    label_gps_pos.grid(row = 0, column = 3, sticky="nsew")
    label_packet_rcv.grid(row = 1, column = 0, sticky="nsew")
    label_packet_loss.grid(row = 1, column = 1, sticky="nsew")
    label_flight_state.grid(row = 1, column = 2, columnspan = 2, sticky="nsew")
    label_cmd_frame.grid(row = 2, column = 0, columnspan = 4, sticky="nsew")

    '''
    
    '''

    # Update CMD label, entry, and button to center them above the graphs
    cmd_frame = tk.Frame(master_temp_label, bg="#FF9797")  # Create a frame to contain the CMD controls
    
    cmd_echo_label = tk.Label(cmd_frame, text=f"Command Echo: {'---'}", font=FONT_TITLE, bg="#FF6060", fg=COLOR_GATOR_ORANGE)

    cmd_frame.grid_columnconfigure(0, weight=1)  # Left spacer
    cmd_frame.grid_columnconfigure(1, weight=0)  # CMD label
    cmd_frame.grid_columnconfigure(2, weight=0, minsize=3)  # CMD entry
    cmd_frame.grid_columnconfigure(3, weight=0)  # Send button
    cmd_frame.grid_columnconfigure(4, weight=1)  # Right Buffer

    cmd_frame.grid(row=2, column=0, columnspan=9,  sticky="ew")  # Span the entire width

    # Create a label for command echo
    cmd_echo_label.grid(row=0, column=0, padx=5, sticky="nsew")

    
    # Add CMD label, entry, and button to the frame
    cmd_label = tk.Label(cmd_frame, text="Command:", font=FONT_TITLE, bg="#FFD447", fg=COLOR_GATOR_ORANGE)
    cmd_label.grid(row=0, column=1, padx=(0, 5), sticky="nsew")

    cmd_entry = tk.Entry(cmd_frame, font=FONT_TITLE, width=20)
    cmd_entry.grid(row=0, column=2, padx=10, sticky="nsew")

    send_button = tk.Button(cmd_frame, text="Send", font=FONT_TITLE, command=send_command, bg="#FF0000")
    send_button.grid(row=0, column=3, padx=0, sticky="nsew")







    # Create mission time label
    mission_time_label = tk.Label(master_temp_label, text="--:--:--", font=FONT_TITLE, bg="#FFFC47", fg=COLOR_GATOR_ORANGE)
    mission_time_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # Create Team ID label
    team_id_label = tk.Label(master_temp_label, text="Team ID: 3174", font=FONT_TITLE, bg="#7EFF47", fg=COLOR_GATOR_ORANGE)
    team_id_label.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    # Create Packet Count label
    packet_count_label = tk.Label(master_temp_label, text="Packet Count: 0", font=FONT_TITLE, bg="#00A824", fg=COLOR_GATOR_ORANGE)
    packet_count_label.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

    # Create Mode label
    mode_label = tk.Label(master_temp_label, text="Mode: IDLE", font=FONT_TITLE, bg="#47EDFF", fg=COLOR_GATOR_ORANGE)
    mode_label.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

    # Create State label
    state_label = tk.Label(master_temp_label, text="State: OK", font=FONT_TITLE, bg="#5347FF", fg=COLOR_GATOR_ORANGE)
    state_label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    # Create Labels for Simulation States
    sim_enable_label = tk.Label(master_temp_label, text="Sim Enable: False", font=FONT_TITLE, bg="#AF47FF", fg=COLOR_GATOR_ORANGE)
    sim_enable_label.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
    sim_active_label = tk.Label(master_temp_label, text="Sim Active: False", font=FONT_TITLE, bg="#FF47A3", fg=COLOR_GATOR_ORANGE)
    sim_active_label.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

    # Create GPS time label
    gps_time_label = tk.Label(master_temp_label, text="--:--:--", font=FONT_TITLE, bg="#780046", fg=COLOR_GATOR_ORANGE)
    gps_time_label.grid(row=1, column=0, padx=5, sticky="nsew")

    #
    ###########################################################################################

    '''

    # Start the Tkinter event loop
    root.mainloop()

    return


###############################################
# Supporting Functions
###############################################

def menuFunc_exit():
    exit()

def menuFunc_about(): #TODO: Fill in text here with proper info
    messagebox.showinfo(
        "About This Application",
        "This is a sample Tkinter application.\n\nVersion: 1.0\nAuthor: CANSAT"
    )
    return

def menuFunc_burger():
    messagebox.showinfo(
        "Bon Appétit",
        "\t🍔\t"
    )

def menuFunc_fries():
    messagebox.showinfo(
        "Bon Appétit",
        "\t🍟\t"
    )

def commandEcho(cmd_string):
    return cmd_string

if __name__ == "__main__":
    main()
    exit()