import tkinter as tk
import socket

address = ('localhost', 6000)

# Create the main window
root = tk.Tk()
root.title("Asynchronous Socket Listening Test")
root.rowconfigure(0, weight=1, uniform='a')
root.columnconfigure(0, weight=1, uniform='a')
# Create and attach label
label_message = tk.Label(root, text="[NO MESSAGE]", background="white", font=("", 50, "bold"))
label_message.grid(row = 0, column = 0, columnspan = 1, rowspan=1, sticky="nw")

# Cross Compatible Zoom
try:
    root.wm_attributes("-zoomed",True) # Linux Version of Zoom
except tk.TclError:
    root.state('zoomed') # Default to the Windows Zoom if the linux fails

# This callback function currently only reads one packet before closing the client connection so the client has to re-connect for every packet sent
def recv_msg_callback(sock, mask):
    
    # Set up the client connection
    client_socket, client_address = sock.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # Read in a message from the client
    msg = client_socket.recv(1024)
    msg = msg.decode("utf-8") # convert bytes to string

    # Update the Tkinter text widget with received data
    label_message.config(text=msg)
    print(f"Received: {msg}")

    # Close the connection
    client_socket.close()

# Create the Socket Object and bind it as well as add it to the tkinter event system
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(address)
sock.listen(0)
root.tk.createfilehandler(sock, tk.READABLE | tk.WRITABLE, recv_msg_callback)

# Start the Tkinter event loop
root.mainloop()

# Delete the filehandler and close the socket connection on the way out
root.tk.deletefilehandler(sock)
sock.close()
