# Libraries and Packages
import tkinter as tk
from tkinter import messagebox

from ctypes import windll

from PIL import Image, ImageTk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


########################## Global Variables ##########################

# Colors and Fonts for Blue and Orange Theme
global COLOR_PRIMARY;           COLOR_PRIMARY = '#F0F0F0'               # Light gray
global COLOR_GATOR_ORANGE;      COLOR_GATOR_ORANGE = "#FA4616"          # Gator Orange
global COLOR_GATOR_BLUE;        COLOR_GATOR_BLUE = "#0021A5"            # Gator Blue
global COLOR_GATOR_GREEN;       COLOR_GATOR_GREEN = "#22884C"           # Gator Green
global COLOR_SSDC_NAVY;         COLOR_SSDC_NAVY = "#001F3C"             # SSDC Navy Blue
global FONT_TITLE;              FONT_TITLE = ("Comic Sans MS", 16, "bold")

######################################################################

def main():
    print("*********************************")
    print("*  Tkinter Grid Testing Python  *")
    print("*      Cansat 2025-2026         *")
    print("*********************************")

    # Create the main window
    root = tk.Tk()

    #windll.shcore.SetProcessDpiAwareness(1) # Make the application DPI aware

    # Add the color and size properties to the main window
    root.title("Tkinter Grid Testing Python Cansat 2025-2026")
    root.configure(bg=COLOR_PRIMARY)
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
    menubar.add_cascade(label="File", menu=menu_file)
    menubar.add_cascade(label="Food", menu=menu_food)
    menubar.add_cascade(label="Help", menu=menu_help)

    # Tack functions to those tabs 
    menu_file.add_command(label="Exit", command=menuFunc_exit)
    menu_help.add_command(label="About", command=menuFunc_about)
    menu_food.add_command(label="Burger", command=menuFunc_burger)
    menu_food.add_command(label="Fries", command=menuFunc_fries)

    # Create widgets
    label1 = tk.Label(root, text="Single Data Info [DEBUG]", background="red")
    label2 = tk.Label(root, text="2D Graphs Field [DEBUG]", background="blue")
    label3 = tk.Label(root, text="3D Graph Field [DEBUG]", background="yellow")

    # Load UF gator logo image data and create widget for it
    imageFile_gators = Image.open("Images/Gators Logo.png")
    imageTk_gators = ImageTk.PhotoImage(imageFile_gators)
    label_gators_logo = tk.Label(root, image=imageTk_gators, background=COLOR_GATOR_GREEN)

    # Load SSDC logo image data and create widget for it
    imageFile_ssdc = Image.open("Images/SSDC Logo green.png")
    imageTk_ssdc = ImageTk.PhotoImage(imageFile_ssdc)
    label_ssdc_logo = tk.Label(root, image=imageTk_ssdc, background=COLOR_GATOR_GREEN)

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

    # Configure the grid
    root.rowconfigure(0, weight=1, uniform='a')
    root.rowconfigure(1, weight=3, uniform='a')
    root.columnconfigure(0, weight=4, uniform='a')
    root.columnconfigure(1, weight=1, uniform='a')
    root.columnconfigure(2, weight=1, uniform='a')

    # Attach the widgets to their grid positions
    label1.grid(row = 0, column = 0, columnspan = 1, rowspan=1, sticky="nsew")
    label2.grid(row = 1, column = 0, columnspan = 1, rowspan=1, sticky="nsew")
    label3.grid(row = 1, column = 1, columnspan = 2, rowspan=1, sticky="nsew")
    label_gators_logo.grid(row=0, column=1, sticky="nsew")
    label_ssdc_logo.grid(row=0, column=2, sticky="nsew")


    ###########################################################################################
    # TEST CODE IN HERE
    ###########################
    #

    #
    ###########################################################################################

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

if __name__ == "__main__":
    main()
    exit()