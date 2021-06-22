"""
ch4t
file: cli_client.py
repository: eli003/ch4t
author: atoby (Tobias König)
"""
import socket
import threading
import sys

host = "127.0.0.1"  # add feature: get from a .gitignore config file
port = 64001  # add feature: get from a .gitignore config file

#Terminal Colors:
look = dict(default='\033[0;0m', logo='\033[38;5;31mch\033[38;5;57m4\033[38;5;31mt\033[0;0m', user='\033[38;5;28m',
            config="\033[38;5;243m", info='\033[38;5;31m', warning='\033[48;5;196m\033[38;5;231m')

def get_config():
    try:
        u = input("{}Before you can start chatting please enter your name: ".format(look['config']))
        ip = input("What IP has the Server? (Format like 'x.x.x.x' or type 'd' for default IP): ")
    except:
        print("Wrong Input") # but what can be wrong tho?

    print(look['default'])

    if ip == "d": #default ip
        host = "127.0.0.1"
    else:
        host = ip
    return u, host

def send_msg(socket):
    while True:
        msg = input("")
        socket.send(msg.encode("cp850"))

def recv_msg(socket):
    while True:
        bytes = s.recv(1024)
        data = bytes.decode("cp850")
        print(data)


##main
if __name__ == '__main__':
    # get config at the beginning
    user, host = get_config()
    print("Welcome {}{}{}, have fun using {}!\n".format(look['user'], user, look['default'], look['logo']))

    #connect with server
    try:
        print("{}Trying to connect to '{}' on port '{}'...{}".format(look['info'],host, port, look['default']))
        s = socket.create_connection((host, port))
        print("{}Connected successfully{}".format(look['info'], look['default']))
    except:
        print("{}Connecting to specified Server failed:{}\n{}Error:".format(look['warning'],
                look['default'], look['warning']), sys.exc_info()[0], look['default'])

    #chatting
    # start two threads: one for sending, one for receiving
    try:
        send = threading.Thread(target=send_msg, args=(s,))
        send.start()
        recv = threading.Thread(target=recv_msg, args=(s,))
        recv.start()

    except:
        print("{}Can't Transmit/Receive{}".format(look['info'], look['default']))

    #finally:
    #    print("\nThanks for using {}! Bye".format(look['logo']))

