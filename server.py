import socket
import threading

HOST = '127.0.0.1'  # localhost
PORT = 12345        # any unused port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f"{name} left the chat.".encode('utf-8'), client)
            names.remove(name)
            break

def receive():
    print("Server is running and listening...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NAME".encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)

        print(f"Name is {name}")
        broadcast(f"{name} joined the chat!".encode('utf-8'), client)
        client.send("Connected to the server!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()