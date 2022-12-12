import socket
import pickle


# This class is used for connecting to our server
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = "172.30.1.20"
        self.port = 8888
        self.address = (self.server_ip, self.port)
        self.IsConnected = False
        self.message = self.connect()
        print(self.message)

    def connect(self):
        try:
            self.client.connect(self.address)  # The client will try to connect to the server
            data = pickle.loads(self.client.recv(2048))  # Receive a pickle object  # The server will the confirmation
            self.IsConnected = True
            return data
        except:
            return "Could not connect to SkyRocket Server. Game is now in offline mode"

    def isClientConnected(self):
        return self.IsConnected

    def SendAndReceive(self, data):
        if self.IsConnected:
            try:
                self.client.settimeout(None)
                self.client.send(pickle.dumps(data))  # Dump it into a pickle object and then send
                return pickle.loads(self.client.recv(8192))  # Receive a pickle object
            except:
                return "Could not receive data from SkyRocket Servers"

    def SendData(self, data):  # Send data to the server
        if self.IsConnected:
            try:
                self.client.send(pickle.dumps(data))  # The client will send data to the server
            except:
                return "Could not send data to SkyRocket Servers"

    def ReceiveData(self):
        if self.IsConnected:
            try:
                self.client.settimeout(0.1)
                return pickle.loads(self.client.recv(2048 * 8))  # Receive a pickle object
            except:
                return None
