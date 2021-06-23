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
class Clients:
    client_list = list()

    def __init__(self, index):
        self.connection, self.client_address = s.accept()
        type(self).client_list.append(self.connection)   # Alle Clients teilen sich die client_list; neue clients
        # werden dieser appended
        self.index = index
        print("Verbundene Clients: ", len(type(self).client_list))

    def send_message(self, message):
        self.connection.send(("Gesendet: %s" % message).encode(codeset))

    def get_message(self):
        while True:
            byte_data = self.connection.recv(1024)
            data = byte_data.decode(codeset)
            print(self.index, 'has send')
            print('received "%s"' % data, file=sys.stderr)
            print('sending data back to the client', file=sys.stderr)
            for cnt, client in enumerate(type(self).client_list):    # nachricht wird nicht an sender gesendet
                if cnt != self.index:
                    client.send(bytes(str(data), 'utf8'))


def get_new_clients(cnt):
    client = Clients(cnt)   # das objekt client der Klasse Clients wird erzeugt
    client.send_message('hallo client\n')   # server sollte eine hallo client message an den neuen client schicken

    t2 = threading.Thread(target=client.get_message)  # thread damit er durchgehend auf neue nachrichten prüft
    t2.start()


s = socket.socket()  # Create a socket object

hostname = socket.gethostbyname_ex(socket.gethostname())[-1]  # IP-Adresse des PCs bestimmen
local_ip = hostname[1]
# print(hostname)
print("IP-Adresse des Servers: ", local_ip)

host = local_ip  # unspecified ip - all interfaces on host
port = 64001  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port
s.listen(10)  # Now wait for client connection.

counter = 0
while True:
    get_new_clients(counter)    # Funktionsaufruf
    counter += 1        # bei jedem neuen client wird der counter erhöht
