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


# Client-class
class Clients(object):
    def __init__(self):
        self.connection, self.client_address = s.accept()

    def send_message(self, message):
        self.connection.sendall(("Gesendet: %s" % message).encode(codeset))

    def get_message(self):
        while True:
            byte_data = self.connection.recv(300)
            data = byte_data.decode(codeset)
            print('received "%s"' % data, file=sys.stderr)
            print('sending data back to the client', file=sys.stderr)
            self.connection.sendall(("server got data: %s" % data).encode(codeset))


'''
s = socket.socket()  # Create a socket object
host = ''  # unspecified ip - all interfaces on host
port = 64001  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(1)  # Now wait for client connection.
new_clients = []
clients = 1
'''


def get_new_clients():
    client = Clients()
    t1 = threading.Thread(target=client.send_message("hallo\n"))
    t1.start()
    t2 = threading.Thread(target=client.get_message())
    t2.start()


s = socket.socket()  # Create a socket object
host = ''  # unspecified ip - all interfaces on host
port = 64001  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port
s.listen(1)  # Now wait for client connection.

t0 = threading.Thread(target=get_new_clients())
t0.start()

while True:
    pass
    # client = Clients()
    # print("Schleife")
    # new_client.send_message()
    # connection, client_address = s.accept()  # Establish / get one connection with client.
#    handle_connection(connection,client_address)   # handle connections one by one
    # or start new thread for each connection
    # print('Got connection from %s' % str(client_address), file=sys.stderr)

    # t1 = threading.Thread(target=client.send_message("hallo\n"))
    # t = threading.Thread(target=handle_connection, args=(connection,))
    # t1.start()
    # t2 = threading.Thread(target=client.get_message())
    # t2.start()
    # and continue with loop accepting next connection
# s.close()
