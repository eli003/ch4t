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
        ip = input("What IP has the Server? ('x.x.x.x' format or type 'd' for default IP ({})): ".format(server))
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
    data = {'user': user, 'msg': ''}

    print("\n{}You can use '-q' to quit the client.{}\n"
          .format(look['info'], look['default']))
    try:
        while True:
            msg = input("{}".format(look['user']))
            print("{}".format(look['default']))

            if msg == "-q":
                stop_client(0)
            else:
                data['msg'] = msg
                byte_data = pickle.dumps(data)
                byte_data = bytes(f"{len(byte_data):<{header_size}}", 'utf-8') + byte_data
                conn.send(byte_data)
                data['msg'] = ''

    except:
        print("{}Error:".format(look['warning']), sys.exc_info()[0], look['default'])

def recv_msg(conn, header_size):
    try:
        while True:
            raw_data = b''
            byte_data = conn.recv(1024)
            raw_data += byte_data
            data = pickle.loads(raw_data[header_size:])
            print("{}{}: {}{}".format(look['other'],data['user'], data['msg'], look['default']))

    except EOFError: #issues if end of pickle is reached... natural error
        pass
    except:
        print("{}Error:".format(look['warning']), sys.exc_info()[0], look['default'])

def inform_server(conn, msg):
    data = {'user': '-toserver', 'msg': msg}

    try:
        byte_data = pickle.dumps(data)
        byte_data = bytes(f"{len(byte_data):<{header_size}}", 'utf-8') + byte_data
        conn.send(byte_data)
        data['msg'] = ''

    except:
        print("{}Error:".format(look['warning']), sys.exc_info()[0], look['default'])

# main
if __name__ == '__main__':
    server = "127.0.0.1" # add feature: get from a .gitignore config file
    port = 64001  # add feature: get from a .gitignore config file
    header_size = 10
    # Terminal Colors:
    look = dict(default='\033[0;0m', logo='\033[38;5;31mch\033[38;5;57m4\033[38;5;31mt\033[0;0m', user='\033[38;5;28m',
                config="\033[38;5;243m", info='\033[38;5;31m', warning='\033[48;5;196m\033[38;5;231m',
                other='\033[38;5;29m' )

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
        inform_server(s, "{} is now online!".format(user))
        send = threading.Thread(target=send_msg, args=(s,user, header_size))
        send.start()
        recv = threading.Thread(target=recv_msg, args=(s, header_size))
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



