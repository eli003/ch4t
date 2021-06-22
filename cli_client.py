#file: cli_client.py
#repository: eli003/ch4t
#date (last modified): 22.06.2021

import socket
import threading

host = "127.0.0.1"  # add feature: get from .gitignore config file
port = 64001  # add feature: get from .gitignore config file

def hell(s):
    print(s)

def get_config():
    try:
        u = input("Before you can start chatting please enter your name: ")
        ip = input("What IP has the Server? (format like 'x.x.x.x' or 'd' for default ip): ")
    except:
        print("Wrong Input")
    return u, ip

def send_msg(socket):
    while True:
        msg = input("")
        socket.send(msg.encode("cp850"))

def recv_msg(socket):
    while True:
        bytes = s.recv(1024)
        data = bytes.decode("UTF-8")
        print(data)


##--main--
if __name__ == '__main__':


        # get config at the beginning
    user, ip = get_config()
    if ip == "d": #default ip
        host = "127.0.0.1"
    else:
        host = ip
    print("Welcome {}".format(user))

    #connect with server

    print("Trying to connect to '{}' on port '{}'".format(host, port))
    s = socket.create_connection((host, port))


    try:
        send = threading.Thread(target=send_msg, args=(s,))
        send.start()

        recv = threading.Thread(target=recv_msg, args=(s,))
        recv.start()
    #start two threads: one for sending, one for receiving
    except:
            print("Cant Transmit/Receive")



    #    print("Wrong network configuration OR no server available")

    #finally:
     #   print("Thanks for using ch4t")

