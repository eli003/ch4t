"""
  ch4t-Server
  file: server_object-oriented.py
  repository: eli003/ch4t
  author: eli003 (Elias Rauth)
  The server of the ch4t-program
  but it's object-oriented now
  !!still under development!!
"""

import socket  # Import socket module
import sys
import threading
import pickle

codeset = 'cp850'  # or 'Latin-1' or 'UTF-8'


# Client-class
class Clients:
    client_list = list()    # All Clients shares the same client_list

    def __init__(self, index):
        self.connection, self.client_address = s.accept()
        type(self).client_list.append(self.connection)  # new clients get appended to the client_list
        self.index = index
        print("Connected Clients: ", len(type(self).client_list))
        print(type(self).client_list)

    def send_client_message_to_all(self, message):
        try:
            for cnt, client in enumerate(type(self).client_list):  # goes through the list of clients
                if cnt != self.index:  # if counter is not the same as the number of the sender: send
                    client.send(bytes(str(message), 'utf8'))  # send the message to another clients
        finally:
            pass

    def send_server_message_to_client(self, message):
        try:
            self.connection.send((message.encode(codeset)))
        finally:
            pass

    def get_message(self):
        try:
            while True:
                full_msg = b''
                byte_data = self.connection.recv(1024)   # incoming message
                full_msg += byte_data
                msg = (pickle.loads(full_msg[header_size:]))
                # msg = byte_data.decode(codeset)   # decoding the message
                print('received "%s" from Client %d' % (msg, self.index), file=sys.stderr)  # who send what message
                self.send_client_message_to_all(msg)
        except(ConnectionAbortedError, ConnectionResetError):
            print("Connection of Client", self.index, "lost!")
            self.index -= 1
            type(self).client_list.remove(self.connection)  # new clients get appended to the client_list


def get_new_clients():
    counter = 0  # for every new client, the counter increases
    while True:
        client = Clients(counter)   # generating the object client of the class Clients
        client.send_server_message_to_client('\nConnected to Server: %s:%s\n' % (local_ip, port))   # server sending msg
        client.send_server_message_to_client('\nYou are now connected to the ch4t-Server!\n'
                                             'Please be nice to other people ;)\n\n')

        t2 = threading.Thread(target=client.get_message)  # thread checking constantly for new messages
        t2.start()
        counter += 1  # counter increases


s = socket.socket()  # Create a socket object

hostname = socket.gethostbyname_ex(socket.gethostname())[-1]  # get the right ip-address of the server
local_ip = hostname[1]
# print(hostname)
print("IP-address of the server: ", local_ip)

host = local_ip  # unspecified ip - all interfaces on host
port = 64001  # Reserve a port for your service.
header_size = 10  # for pickle to load
s.bind((host, port))  # Bind to the port
s.listen(10)  # Now wait for client connection.

get_new_clients()    # function call for checking for new clients
