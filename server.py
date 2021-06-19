"""
  ch4t-Server
  The server of the ch4t-programm
  Written by Elias Rauth
"""

import socket  # Import socket module
import sys
import threading
import json

codeset = 'cp850'  # or 'Latin-1' or 'UTF-8'

def handle_connection(connection):
    try:
        # Receive the data in small chunks and retransmit it
        while True:
            byte_data = connection.recv(300)
            data = byte_data.decode(codeset)
            print('received "%s"' % data, file=sys.stderr)
            print('sending data back to the client', file=sys.stderr)
            connection.sendall(("server got data: %s" % data).encode(codeset))
    except (ConnectionAbortedError, ConnectionResetError ):
        pass
    except:
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        connection.close()
        # Clean up the connection


s = socket.socket()  # Create a socket object
host = ''  # unspecified ip - all interfaces on host
port = 64001  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(1)  # Now wait for client connection.

while True:
    connection, client_address = s.accept()  # Establish / get one connection with client.
#    handle_connection(connection,client_address)   # handle connections one by one
    # or start new thread for each connection
    print('Got connection from %s' % str(client_address), file=sys.stderr)

    t=threading.Thread(target=handle_connection,args=(connection,))
    t.start()
    # and continue with loop accepting next connection
#s.close()