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
    client_list = list()    # All Clients shares the same client_list

    def __init__(self, index):
        self.connection, self.client_address = s.accept()
        type(self).client_list.append(self.connection)  # new clients get appended to the client_list
        self.index = index
        print("Verbundene Clients: ", len(type(self).client_list))
        print(type(self).client_list)

    def send_client_message_to_all(self, message):
        # self.connection.send(("Gesendet: %s" % message).encode(codeset))
        for cnt, client in enumerate(type(self).client_list):  # goes through the list of clients
            if cnt != self.index:  # if counter is not the same as the number of the sender: send
                client.send(bytes(str(message), 'utf8'))  # send the message to another clients

    def send_server_message_to_client(self, message):
        self.connection.send((message.encode(codeset)))

    def get_message(self):
        while True:
            byte_data = self.connection.recv(1024)   # incoming message
            data = byte_data.decode(codeset)   # decoding the message
            print('received "%s" from %d' % (data, self.index), file=sys.stderr)  # print who send what message
            self.send_client_message_to_all(data)
            # print('received "%s" from %d' % (data, self.index), file=sys.stderr)  # print who send what message
            # for cnt, client in enumerate(type(self).client_list):    # goes through the list of clients
                # if cnt != self.index:   # if counter is not the same as the number of the sender: send
                    # client.send(bytes(str(data), 'utf8'))  # send the message to another clients


def get_new_clients(cnt):
    client = Clients(cnt)   # generating the object client of the class Clients
    client.send_server_message_to_client('\nConnected to Server: %s:%s\n' % (local_ip, port))   # server sending message
    client.send_server_message_to_client('\nYou are now connected to the ch4t-Server!\n'
                                         'Please be nice to other people ;)\n\n')

    t2 = threading.Thread(target=client.get_message)  # thread checking constantly for new messages
    t2.start()


s = socket.socket()  # Create a socket object

hostname = socket.gethostbyname_ex(socket.gethostname())[-1]  # get the right ip-address of the server
local_ip = hostname[1]
# print(hostname)
print("IP-Adresse des Servers: ", local_ip)

host = local_ip  # unspecified ip - all interfaces on host
port = 64001  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port
s.listen(10)  # Now wait for client connection.

counter = 0
while True:
    get_new_clients(counter)    # function call for checking for new clients
    counter += 1        # for every new client, the counter increases
