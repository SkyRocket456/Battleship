import socket
# Allows connections to come into the server on a certain port
import threading
# Allow multiple processes to be happening simultaneously
import pickle
# Allows clients and servers to communicate through objects
from server_functions.Queue_System import Queue
from server_functions.ServerLog import ServerLog
from server_functions.server_client_threads import Client_In_Username_Screen

server = "10.145.16.29"
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET and SOCK_STREAM are just a type of connection
# AF_INET is to connect to an IPv4 address
# SOCK_STREAM means that it is a TCP socket.

try:  # Used to see if the port 5555 is being used for something else
    s.bind((server, port))  # Binds the server to the port
except socket.error as e:
    print(e)


s.listen()  # Listens for connections
print("Waiting for new players to connect to the server...\n")

Log = threading.Thread(target=ServerLog, args=())
Log.start()

Battleship_Queue = threading.Thread(target=Queue, args=())
Battleship_Queue.start()

while True:
    conn, address = s.accept()
    # Accept any incoming connection
    # conn is an object holding information of the connection
    # address is the ip address
    conn.send(pickle.dumps("Connected to SkyRocket Servers"))  # Send confirmation message back to client
    Client_Server_Communication = threading.Thread(target=Client_In_Username_Screen, args=(conn, address))
    Client_Server_Communication.start()

