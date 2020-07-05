import socket
import threading

PORT = 5050
SERVER = "192.168.10.104"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
MSG_LENGTH = 4096

class MyClient:
    def __init__(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)
            self.connected = True
        except (ConnectionResetError, ConnectionRefusedError) as e:
            print(e)
            self.connected = False
        
        self.history = []
        
    def start_reciever(self):
        # recieve messages from server
        thread = threading.Thread(target=self.recieve)
        thread.start()
                
    def recieve(self):
        while self.connected:
            msg = self.client.recv(MSG_LENGTH).decode()
            self.history.append(msg)
            
    def send(self, msg):
        try:
            self.client.send(msg.encode())
            if msg == DISCONNECT_MESSAGE:
                self.connected = False
        except ConnectionResetError:
            self.history.append("DISCONNECTED")
            self.connected = False