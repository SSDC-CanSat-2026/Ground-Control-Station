import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


########################## Global Variables ##########################

# Colors and Fonts for Blue and Orange Theme
global PRIMARY_COLOR;   PRIMARY_COLOR = '#F0F0F0'   # Light gray
global GATOR_ORANGE;    GATOR_ORANGE = '#FA4616'      # Gator Orange
global GATOR_BLUE;      GATOR_BLUE = "#0021A5"      # Gator Blue
global FONT_TITLE;      FONT_TITLE = ("Verdana", 16, "bold")

######################################################################

def menu_exit():
    exit()

def menu_about(): #TODO: Fill in text here with proper info
    messagebox.showinfo(
        "About This Application",
        "This is a sample Tkinter application.\n\nVersion: 1.0\nAuthor: CANSAT"
    )
    return

def main():
    print("*********************************")
    print("*  Tkinter Grid Testing Python  *")
    print("*      Cansat 2025-2026         *")
    print("*********************************")

    # Create the main window
    root = tk.Tk()
    root.title("Tkinter Grid Testing Python Cansat 2025-2026")
    root.configure(bg=PRIMARY_COLOR)

    width= root.winfo_screenwidth() 
    height= root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.state('zoomed') #Automatically Maximize Window

    # Other window sizing methods
    #root.geometry("1000x700")  # Set a fixed window size
    #root.attributes("-fullscreen", True)
    #root.geometry("%dx%d" % (width, height))

    # Create the main menubar and assign as the root's menu
    menubar = tk.Menu(root)
    root.config(menu=menubar) # Attach the menubar to the root window
    
    # Define all the menu tabs functions in the main scope so that they have access to menu_burger_draw_image()
    def menu_burger_crown():
        menu_burger_draw_image("Images/Crown.png")

    def menu_burger_sauce():
        menu_burger_draw_image("Images/Sauce.png")

    def menu_burger_onions():
        menu_burger_draw_image("Images/Onions.png")

    def menu_burger_tomato():
        menu_burger_draw_image("Images/Tomato.png")

    def menu_burger_lettuce():
        menu_burger_draw_image("Images/Lettuce.png")

    def menu_burger_cheese():
        menu_burger_draw_image("Images/Cheese.png")

    def menu_burger_patty():
        menu_burger_draw_image("Images/Patty.png")

    def menu_burger_heel():
        menu_burger_draw_image("Images/Heel.png")

    # Define the menu_burger_draw_image() function in main scope so that it has access to the root variable    
    def menu_burger_draw_image(image_path):
    
        popup = tk.Toplevel(root)  # Create a Toplevel window

        # Load the image using PIL
        try:
            img = Image.open(image_path)
            # Optional: Resize the image if needed
            # img = img.resize((width, height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            tk.messagebox.showerror("Error", f"Image not found at: {image_path}")
            return

        # Create a Label to display the image
        image_label = tk.Label(popup, image=photo)
        image_label.image = photo  # Keep a reference to prevent garbage collection
        image_label.pack(padx=10, pady=10)

        image_label.configure(bg='#FFFFFF')
        popup.configure(bg='#FFFFFF')
    
        # Optional: Add a close button
        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=5)

    # Create menu bar objects
    file_menu = tk.Menu(menubar, tearoff=False)
    burger_menu = tk.Menu(menubar, tearoff=False)
    help_menu = tk.Menu(menubar, tearoff=False)
    
    # Create tabs from those objects
    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Burger", menu=burger_menu)
    menubar.add_cascade(label="Help", menu=help_menu)

    # Tack functions to those tabs 
    file_menu.add_command(label="Exit", command=menu_exit)
    help_menu.add_command(label="About", command=menu_about)
    burger_menu.add_command(label="Crown", command=menu_burger_crown)
    burger_menu.add_command(label="Sauce", command=menu_burger_sauce)
    burger_menu.add_command(label="Onions", command=menu_burger_onions)
    burger_menu.add_command(label="Tomato", command=menu_burger_tomato)
    burger_menu.add_command(label="Lettuce", command=menu_burger_lettuce)
    burger_menu.add_command(label="Cheese", command=menu_burger_cheese)
    burger_menu.add_command(label="Patty", command=menu_burger_patty)
    burger_menu.add_command(label="Heel", command=menu_burger_heel)

    ###########################################################################################
    # TEST CODE IN HERE
    ###########################
    #

    #create widgets
    label1 = tk.Label(root, text="Single Data Info [DEBUG]", background="red")
    label2 = tk.Label(root, text="2D Graphs Field [DEBUG]", background="blue")
    label3 = tk.Label(root, text="3D Graph Field [DEBUG]", background="yellow")

    #configure grid
    root.rowconfigure(0, weight=1, uniform='a')
    root.rowconfigure(1, weight=4, uniform='a')
    root.columnconfigure(0, weight=2, uniform='a')
    root.columnconfigure(1, weight=1, uniform='a')

    #attach the widgets to their grid positions
    label1.grid(row = 0, column = 0, columnspan = 2, rowspan=1, sticky="nsew")
    label2.grid(row = 1, column = 0, columnspan = 1, rowspan=1, sticky="nsew")
    label3.grid(row = 1, column = 1, columnspan = 1, rowspan=1, sticky="nsew")

    #
    ###########################################################################################

    # Start the Tkinter event loop
    root.mainloop()

    return

if __name__ == "__main__":
    main()
    exit()