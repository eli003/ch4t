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


# Client-class
class Clients:
    client_list = list()  # All Clients shares the same client_list
    id_list = list()   # List of client_id's that are online

    def __init__(self, client_id):
        self.connection, self.client_address = s.accept()
        self.client_list.append(self.connection)  # new clients get appended to the client_list
        self.client_id = client_id
        self.id_list.append(self.client_id)     # the id of new clients get appended to the id_list
        print("Connected Clients: ", len(self.client_list))
        print(self.client_list)

    def send_client_message_to_all(self, message, client_number):
        try:
            for client, ID in zip(self.client_list, self.id_list):  # goes through the list of clients and id_list
                if client_number != ID:  # if sender_id is not the same as the actual id -> send
                    byte_data = pickle.dumps(message)
                    byte_data = bytes(f"{len(byte_data):<{header_size}}", 'utf-8') + byte_data
                    client.send(byte_data)   # send the message to another clients
                    print("sent to client", self.client_id)
        finally:
            pass

    def send_server_message_to_client(self, message):
        data = {'user': "Server", 'msg': message}
        byte_data = pickle.dumps(data)
        byte_data = bytes(f"{len(byte_data):<{header_size}}", 'utf-8') + byte_data
        try:
            self.connection.send(byte_data)
        finally:
            pass

    def send_server_message_to_all(self, message, client_number):
        data = {'user': "Server", 'msg': message}
        try:
            print(client_number)
            for client, ID in zip(self.client_list, self.id_list):  # goes through the list of clients and id_list
                if client_number != ID:  # if sender_id is not the same as the actual id -> send
                    byte_data = pickle.dumps(data)
                    byte_data = bytes(f"{len(byte_data):<{header_size}}", 'utf-8') + byte_data
                    client.send(byte_data)   # send the message to another clients
                print("server_broadcast")
        finally:
            pass

    def receive_message(self):
        try:
            while True:
                full_msg = b''
                byte_data = self.connection.recv(1024)  # incoming message
                full_msg += byte_data
                msg = (pickle.loads(full_msg[header_size:]))

                print('received "%s" from Client %d' % (msg, self.client_id), file=sys.stderr)  # who send what message
                if msg['user'] == '-toserver':
                    self.send_server_message_to_all(msg['msg'], self.client_id)
                else:
                    self.send_client_message_to_all(msg, self.client_id)  # sending unloaded pickle to other clients
        except(ConnectionAbortedError, ConnectionResetError):
            print("Connection of Client", self.client_id, "lost!")
            self.client_list.remove(self.connection)  # leaving clients getting removed from client_list
            self.id_list.remove(self.client_id)
            print("Connected Clients: ", len(self.client_list))
            print(self.client_list)


def get_new_clients():
    counter = 1  # for every new client, the counter increases
    while True:
        client = Clients(counter)  # generating the object client of the class Clients
        client.send_server_message_to_client('\nConnected to Server: %s:%s\n\nYou are now connected to the '
                                             'ch4t-Server!\nPlease be nice to other people ;)\n\n' % (local_ip, port))
        # server sending hello-msg

        t2 = threading.Thread(target=client.receive_message)  # thread checking constantly for new messages
        t2.start()
        counter += 1  # counter increases


if __name__ == '__main__':
    s = socket.socket()  # Create a socket object

    hostname = socket.gethostbyname_ex(socket.gethostname())[-1]  # get the right ip-address of the server
    local_ip = hostname[1]
    # print(hostname)
    print("IP-address of the server: ", local_ip)

    host = local_ip  # interface of the server
    port = 64001  # Reserve a port for your service.
    header_size = 10  # for pickle to load and dump
    s.bind((host, port))  # Bind to the port
    s.listen(10)  # Now wait for client connection.

    get_new_clients()  # function call for checking for new clients
