import socket
from _thread import *
import sys

server = "192.168.74.129"
port = 5555

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket1.bind((server, port))
except socket.error as e:
    str(e)

socket1.listen(2)
print("Server has started, connecting...")

def threaded_client(connection):
    connection.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = connection.recv(2048)
            reply = data.encode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Recieved: ", reply)
                print("Sending: ", reply)
            
            connection.sendall(str.encode(reply))
        except:
            break
    
    print("Connection lost")

while True:
    connection, addr = socket1.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (connection,))