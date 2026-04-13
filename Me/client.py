import socket
import os

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))
print("Connected to the Server")

filename = input("Enter filename you would like to download: ")

client_socket.send(filename.encode())

responce = client_socket.recv(1024).decode()

if responce == "OK":
    print("Server has found the file! Initializing download...")
    file_size = int(client_socket.recv(1024).decode())

    bytes_recevied = 0
    with open(filename, "wb") as f:
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            f.write(chunk)
            bytes_recevied += len(chunk)

            progress = (bytes_recevied/file_size) * 100
            print(f"Downloading.... {progress:.1f}%", end="\r")
        
    print("\nDownload Complete!")
    client_socket.close()
else:
    print(f"Server says: {responce}")
    client_socket.close()
