import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
MSG_LENGTH = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")
    clients.append((conn, addr))
    print(f"[CONNECTED USERS] {threading.activeCount() - 1}")
    conn.send(f"[SERVER] You are {addr}.".encode())
    send_everyone(f"[SERVER] {addr} joined.")
    
    connected = True
    while connected:
        msg = conn.recv(MSG_LENGTH).decode()
        if msg == DISCONNECT_MESSAGE:
            connected = False
        print(f"[{addr}] {msg}")
        
        send_everyone(f"[{addr[0]} {addr[1]}] {msg}")
        
    clients.remove((conn, addr))
    conn.close()
    print(f"[CLOSING CONNECTION] {addr}")

def send_everyone(msg):
    for client_conn, client_addr in clients:
        client_conn.send(msg.encode())

def start():
    print("Starting server...")
    server.listen()
    print("Listening...\n")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

print(f"[SERVER] {SERVER}")
start()