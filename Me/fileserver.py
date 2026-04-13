import socket
import os

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server is waiting for a connection...")

client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

filename =  client_socket.recv(1024).decode()
print(f"Client requested file: {filename}")

if os.path.exists(filename):
    client_socket.send("OK".encode())
    print(f"Filename :'{filename}'found. Sending...")

    file_size = os.path.getsize(filename)
    client_socket.send(str(file_size).encode())

    with open(filename, "rb") as f:
        bytes_sent = 0
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            client_socket.send(chunk)
            bytes_sent += 1024

        print("File Transfer Successful")
else:
    client_socket.send("File doees not exist".encode())
    print("File not found. Notifying client.")


client_socket.close()
server_socket.close()