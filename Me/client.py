"""
CS310 Assignment 1 - File Transfer Client
Student Name and ID: Surbhit Nand (S11230283)
                     Parvish Mohan (S11230414)

This client connects to 127.0.0.1:5000, requests a file by name, receives the
server response, shows the download progress percentage, and saves the file in
its working directory with a "_downloaded" suffix.
"""

import socket
import os

HOST = "127.0.0.1"
PORT = 5000

try:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clientSocket.connect((HOST, PORT))

    print(f"[CLIENT] Connected to server at {HOST}:{PORT}")

    filename = input("Enter the filename to download: ")
    #Validation Check
    if not filename:
        print("[CLIENT] No filname entered. Closing connection")
        clientSocket.close()
        exit()

    clientSocket.send(filename.encode())
    print(f"[CLIENT] Requested file: '{filename}'")


    response = clientSocket.recv(1024).decode()

    if response == "OK":
        file_size = int(clientSocket.recv(1024).decode())
        print(f"[CLIENT] Server acknowledged. File size: {file_size} bytes.")
        print(f"[CLIENT] Starting download...")

        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_downloaded{ext}"

        try:
            bytes_received = 0

            with open(new_filename, "wb") as f:
                while True:
                    chunk = clientSocket.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_received += len(chunk)
                    progress = (bytes_received / file_size) * 100
                    print(f"[CLIENT] Downloading... {progress:.0f}%", end="\r")

            print(f"\n[CLIENT] Download complete. File saved as '{new_filename}'.")
            print(f"[CLIENT] File transfer successful.")

        except IOError as e:
            print(f"[CLIENT] File I/O error: {e}")

    else:
        print(f"[CLIENT] Server says: {response}")

except socket.error as e:
    print(f"[CLIENT] Connection error: {e}")
    print(f"[CLIENT] Make sure the server is running before starting the client.")

finally:
    clientSocket.close()
    print(f"[CLIENT] Connection closed.")