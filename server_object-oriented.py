"""
  ch4t-Server
  The server of the ch4t-programm
  Written by Elias Rauth
"""

import socket  # Import socket module
import sys
import threading

codeset = 'cp850'  # or 'Latin-1' or 'UTF-8'

s = socket.socket()  # Create a socket object
host = ''  # unspecified ip - all interfaces on host
port = 64001  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(1)  # Now wait for client connection.


# Client-class
class Client(object):
    def __init__(self, name="unknown name"):
        self.client_name = name
