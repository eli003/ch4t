"""
ch4t
file: cli_client.py
repository: eli003/ch4t
author: atoby (Tobias König)
"""
import socket
import threading
import os
import sys
import pickle

def get_config(server):
    try:
        u = input("{}Before you can start chatting please enter your name: ".format(look['config']))
        ip = input("What IP has the Server? ('x.x.x.x' format or type 'd' for default IP): ")
    except:
        print("Wrong Input") # but what can be wrong tho?


    print(look['default'])

    if ip == "d": #default ip
        host = server
    else:
        host = ip
    return u, host

def stop_client(exit_code):
    print("\nThanks for using {}! Bye".format(look['logo']))
    os._exit(exit_code)

def send_msg(conn, user, header_size):
    send_data = {'user' : [], 'msg' : []}
    send_data['user'].append(user)
    try:
        print("\n{}You can use '-q' to quit the client.{}\n"
              .format(look['info'], look['default']))
        while True:
            msg = input("{}Me: ".format(look['user']))
            print("{}".format(look['default']))

            if msg == "-q":
                stop_client(0)
            else:
                send_data['msg'].append(msg)
                byte_send_data = pickle.dumps(send_data)
                byte_send_data = bytes(f"{len(byte_send_data):<{header_size}}", 'utf-8') + byte_send_data
                conn.send(byte_send_data)
                send_data['msg'].clear()

    except:
        print("{}Error:".format(look['warning']), sys.exc_info()[0], look['default'])

def recv_msg(conn):
    try:
        while True:
            bytes = conn.recv(1024)
            data = bytes.decode("cp850")
            print(data)
    except:
        print("{}Error:".format(look['warning']), sys.exc_info()[0], look['default'])
    finally:
        print("\nThanks for using {}! Bye".format(look['logo']))

##main
if __name__ == '__main__':
    server = "127.0.0.1" # add feature: get from a .gitignore config file
    port = 64001  # add feature: get from a .gitignore config file
    header_size = 10
    # Terminal Colors:
    look = dict(default='\033[0;0m', logo='\033[38;5;31mch\033[38;5;57m4\033[38;5;31mt\033[0;0m', user='\033[38;5;28m',
                config="\033[38;5;243m", info='\033[38;5;31m', warning='\033[48;5;196m\033[38;5;231m')

    # get config at the beginning
    user, host = get_config(server)
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
        send = threading.Thread(target=send_msg, args=(s,user, header_size))
        send.start()
        recv = threading.Thread(target=recv_msg, args=(s,))
        recv.start()

    except:
        print("{}Can't connect to Server, please check your connection.{}".format(look['info'], look['default']))
        """restart = input("{}\nRestart the program? (y/n) {}".format(look['config'], look['default']))
        if restart == "y":
            try:
                python = sys.executable
                os.execv(python, python, *sys.argv)
            except:
                print("{}Can't restart the program.{}".format(look['info'], look['default']))
                stop_client()
        else:"""
        stop_client(1)



