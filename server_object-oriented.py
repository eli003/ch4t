"""
  ch4t-Server
  The server of the ch4t-programm
  but it's object-oriented now
  !!still under development!!
  Written by Elias Rauth
"""

import socket  # Import socket module
import sys
import threading

codeset = 'cp850'  # or 'Latin-1' or 'UTF-8'
clients = 0

# Client-class
class Client(object):
    def __init__(self):
        self.connection, self.client_address = s.accept()

    def send_message(self, message):
        self.connection.sendall(("Gesendet: %s" % message).encode(codeset))

    def get_message(self):
        pass


s = socket.socket()  # Create a socket object
host = ''  # unspecified ip - all interfaces on host
port = 64001  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(1)  # Now wait for client connection.

while True:
    new_client = Client()
    # new_client.send_message()
    # connection, client_address = s.accept()  # Establish / get one connection with client.
#    handle_connection(connection,client_address)   # handle connections one by one
    # or start new thread for each connection
    # print('Got connection from %s' % str(client_address), file=sys.stderr)

    t = threading.Thread(target=new_client.send_message("hallo"))
    # t = threading.Thread(target=handle_connection, args=(connection,))
    t.start()
    # and continue with loop accepting next connection
# s.close()
