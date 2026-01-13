import socket
import time

address = ('localhost', 6000)

# Packet sending function (Because the listener only accepts one packet per connection, every call of this function makes a connection)
def send_msg(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.send(msg.encode('utf-8'))
    print("Sent:",msg)
    sock.close()

# Test Messages
msgs = ["Hi","How","Are","You?","[END]"]

for msg in msgs:
    send_msg(msg)
    time.sleep(1)
