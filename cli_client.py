#file: cli_client.py
#repository: eli003

import socket

host = "127.0.0.1"
port = 64001

s=socket.create_connection(("localhost",port))

s.send("Hallo Tobias König".encode("cp850"))   # write data
bytes=s.recv(1024)          # receive data
print("Response from server:",bytes.decode("cp850"))      # decode and output received data
s.close()                   # Close the socket when done