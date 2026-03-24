import tkinter as tk
import socket
import time
import threading

HOST = 'localhost'
PORT_P = 6000
PORT_G = 6001
ADDRESS_P = (HOST, PORT_P)
ADDRESS_G = (HOST, PORT_G)

class TelemetryHandler:

    def __init__(self):

        self.is_running = True

    def start_telemetry(self):

        print("Handler Started")

        # Create the two threads, one for monitoring the incoming commands and one for running the main execution loop that sends data to the GUI
        self.receive_thread = threading.Thread(target=self._monitor_incoming, daemon=True)
        self.receive_thread.start()
        self.send_thread = threading.Thread(target=self._loop_outgoing, daemon=True)
        self.send_thread.start()

        return

    def stop_telemetry(self):
        
        self.is_running = False

        self.receive_thread.join()
        self.receive_thread.join()

        return

    def _monitor_incoming(self):

        sock_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_in.bind(ADDRESS_P)
        sock_in.listen(0)
        sock_in.settimeout(2)

        while (self.is_running):
            try:
                conn, addr = sock_in.accept()
                full_data = ""
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    full_data += data.decode('utf-8')
                conn.close()
                print("PROC Recv:", full_data)
            except socket.timeout:
                #print("Socket Timout")
                1==1

    def _loop_outgoing(self):

        time.sleep(1)
        i = 1

        while (self.is_running == True):
            # Write to the socket instead 
            time.sleep(1)
            #print("LOOP OUTGOING")

            line = str(i)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if (not sock.connect_ex(ADDRESS_G)):    
                sock.send(line.encode('utf-8'))
                print("Proc Sent:", line, end="\t")
                i += 1
            else:
                #print("Proc Failed Send")
                1==1

            sock.close()

def gui():

    def send_msg_callback():
        # First send some data
        msg = "Hi"
        sock_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_out.connect(ADDRESS_P)
        sock_out.send(msg.encode('utf-8'))
        sock_out.close()
        print("GUI Sent:", msg, end="\t")

    # This callback function currently only reads one packet before closing the client connection so the client has to re-connect for every packet sent
    def recv_msg_callback(sock, mask):
        
        # Set up the client connection
        client_socket, client_address = sock.accept()
        #print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        # Read in a message from the client
        msg = client_socket.recv(1024)
        msg = msg.decode("utf-8") # convert bytes to string

        # Update the Tkinter text widget with received data
        label_message.config(text=msg)
        print(f"GUI Recv: {msg}")

        # Close the connection
        client_socket.close()

    print("GUI Started")
    time.sleep(1)

    # Create the main window
    root = tk.Tk()
    root.title("Asynchronous Socket Send/Rcv Test")
    root.rowconfigure(0, weight=1, uniform='a')
    root.rowconfigure(1, weight=1, uniform='a')
    root.columnconfigure(0, weight=1, uniform='a')
    # Create and attach label
    label_message = tk.Label(root, text="[NO MESSAGE]", background="white", font=("", 50, "bold"), wraplength= root.winfo_screenwidth() * 0.9, justify=tk.LEFT) # Align text to the left)
    label_message.grid(row = 0, column = 0, columnspan = 1, rowspan=1, sticky="nw")
    label_button = tk.Button(root, text="[Send Hi]", background="white", font=("", 50, "bold"), command=send_msg_callback)
    label_button.grid(row = 1, column = 0, columnspan = 1, rowspan=1, sticky="news")

    # Initialize the sockets
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_in.bind(ADDRESS_G)
    sock_in.listen(0)

    # Add socket to the tkinter event system
    root.tk.createfilehandler(sock_in, tk.READABLE | tk.WRITABLE, recv_msg_callback)

    # Start the Tkinter event loop
    root.mainloop()

    # Delete the filehandler and close the socket connection on the way out
    root.tk.deletefilehandler(sock_in)
    sock_in.close()
  
    return

if __name__ == "__main__":
    handler = TelemetryHandler()
    handler.start_telemetry()
    time.sleep(5)
    gui()
    handler.stop_telemetry()
