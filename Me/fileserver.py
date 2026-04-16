"""
CS310 Assignment 1 - File Transfer Server
Student Name and ID: Surbhit Nand (S11230283)
                     Parvish Mohan (S11230414)

This server listens on 127.0.0.1:5000, validates file requests from the client,
and transmits the file in chunks if it exists.
"""

import socket
import os

HOST = "127.0.0.1"
PORT = 5000

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    serverSocket.bind((HOST, PORT))

    serverSocket.listen(1)
    
    print(f"[SERVER] Listening on {HOST}:{PORT}")
    print(f"[SERVER] Waiting for a connection...")

    clientSocket, client_address = serverSocket.accept()
    print(f"[SERVER] Connected to client at {client_address}.")

    filename = clientSocket.recv(1024).decode()
    print(f"[SERVER] Client requested file: '{filename}'")

    if os.path.exists(filename):
        clientSocket.send("OK".encode())
        print(f"[SERVER] File '{filename}' found.")

        file_size = os.path.getsize(filename)
        clientSocket.send(str(file_size).encode())
        print(f"[SERVER] Sending file. Size: {file_size} bytes.")

        try:
            with open(filename, "rb") as f:
                bytes_sent = 0
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    clientSocket.send(chunk)
                    bytes_sent += len(chunk)
                    progress = (bytes_sent / file_size) * 100
                    print(f"[SERVER] Uploading... {progress:.0f}%", end="\r")

            print(f"\n[SERVER] File transfer successful.")

        except IOError as e:
            print(f"[SERVER] File I/O error: {e}")

    else:
        clientSocket.send("File does not exist".encode())
        print(f"[SERVER] File '{filename}' not found. Notifying client.")

except socket.error as e:
    print(f"[SERVER] Socket error: {e}")

finally:
    try:
        clientSocket.close()
    except:
        pass
    serverSocket.close()
    print(f"[SERVER] Server closed.")