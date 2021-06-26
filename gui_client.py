"""
ch4t
file: gui_client.py
repository: eli003/ch4t
author: eli003 (Elias Rauth)
"""

import tkinter
import socket
import threading
import os
import sys
import pickle
import ctypes

WINDOWCOLOR = "white"

class GUIClient(tkinter.Tk):
    def __init__(self, connection=None, user=None, header_size=10):
        super().__init__()
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Fix Screen Resolution
        self.conn = connection
        self.user = user
        self.header_size = header_size
        self.title("ch4t Client")
        self.minsize(500, 540)
        self.resizable(False, False)
        self.geometry("+%d+%d" % (700, 200))
        self.config(bg=WINDOWCOLOR)
        # Programelements
        # name-label
        self.namelabel()
        self.spacefield()
        # chat-window
        self.chat_window()
        self.spacefield()
        # entry-field
        self.entry_field()

        self.recv = threading.Thread(target=self.receive_msg)
        self.recv.start()
        self.kill_thread = False

    def spacefield(self):
        space = tkinter.Label(self, text="", bg=WINDOWCOLOR)
        space.pack()

    def namelabel(self):
        program_name = tkinter.Label(self, text="ch4t Client", fg="white", font="Arial", bg="goldenrod")
        program_name.pack(fill="both")

    def chat_window(self):
        self.chats = ["Start"]
        self.scrollbar = tkinter.Scrollbar(self)
        self.chatbox = tkinter.Listbox(self, width=80, height=26, bd=4)
        self.chatbox.insert("end", *self.chats)
        self.scrollbar.pack(side="right", fill="y")
        self.chatbox.pack()
        self.chatbox["yscrollcommand"] = self.scrollbar.set
        self.scrollbar["command"] = self.chatbox.yview

    def entry_field(self):
        entryfield = tkinter.Frame(self)
        self.entry_msg = tkinter.StringVar()
        self.entry_msg.set("")
        self.chat_entry = tkinter.Entry(entryfield, width=60, bd=4)
        self.chat_entry["text"] = self.entry_msg
        # self.chat_entry.bind("<Return>", self.send_msg_enter)
        send_button = tkinter.Button(entryfield, text="send message",
                                     command=lambda: self.send_msg(self.conn, self.user, self.header_size))
        self.chat_entry.grid(row=0, column=0)
        send_button.grid(row=0, column=1)
        entryfield.pack()

    def send_msg_enter(self, event):
        print(self.entry_msg.get())

    def send_msg(self, conn, user, header_size):
        print(self.entry_msg.get())
        msg = self.entry_msg.get()
        data = {'user': user, 'msg': ''}
        try:
            if msg == "-q":
                stop_client(0)
            else:
                data['msg'] = msg
                byte_data = pickle.dumps(data)
                byte_data = bytes(f"{len(byte_data):<{header_size}}", 'utf-8') + byte_data
                conn.send(byte_data)
                self.chatbox.insert("end", "Du: {}".format(data['msg']))
                data['msg'] = ''
                self.entry_msg.set("")
        finally:
            pass

    def receive_msg(self):
        try:
            while True:
                raw_data = b''
                byte_data = self.conn.recv(1024)
                raw_data += byte_data
                data = pickle.loads(raw_data[self.header_size:])
                print(data)
                # self.chats.append("{}: {}".format(data['user'], data['msg']) + "\n")
                self.chatbox.insert("end", "{}: {}".format(data['user'], data['msg']))
                if self.kill_thread:
                    break

        except EOFError:  # issues if end of pickle is reached... natural error
            pass
        except ConnectionResetError:
            print("{}Server offline.{}".format(look['info'], look['default']))
            stop_client(3)
        except:
            print("{}Error:".format(look['warning']), sys.exc_info()[0], look['default'])




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

'''
def send_msg(conn, user, header_size):
    data = {'user': user, 'msg': ''}

    print("\n{}You can use '-q' to quit the client.{}\n"
          .format(look['info'], look['default']))
    try:
        while True:
            msg = input("{}".format(look['user']))
            #print("{}".format(look['default']))

            if msg == "-q":
                stop_client(0)
            else:
                data['msg'] = msg
                byte_data = pickle.dumps(data)
                byte_data = bytes(f"{len(byte_data):<{header_size}}", 'utf-8') + byte_data
                conn.send(byte_data)
                data['msg'] = ''

    except ConnectionResetError:
        print("{}Server offline.{}".format(look['info'], look['default']))
        stop_client(3)
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
    except ConnectionResetError:
        print("{}Server offline.{}".format(look['info'], look['default']))
        stop_client(3)
    except:
        print("{}Error:".format(look['warning']), sys.exc_info()[0], look['default'])
'''
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

    gui_window = GUIClient(s, user, 10)

    #chatting
    # start two threads: one for sending, one for receiving
    try:
        inform_server(s, "{} is now online!".format(user))
        # send = threading.Thread(target=gui_window.send_msg, args=(s,user, header_size))
        # send.start()
        # recv = threading.Thread(target=gui_window.receive_msg)
        # recv.start()

    except:
        print("{}Can't connect to Server, please check your connection.{}".format(look['info'], look['default']))
        stop_client(1)

    gui_window.mainloop()
    # gui_window.kill_thread = True
    # gui_window.recv.join()
