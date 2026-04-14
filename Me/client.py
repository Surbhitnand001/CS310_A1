# Authors: Surbhit Nand(S11230283), Parvish Mohan(S11230414)

import socket
import os

HOST = "127.0.0.1" #IPV4
PORT = 5000          

try:
    #Determines the type of IP addres and Protocol to use
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connects socket through the PORT to the HOST
    clientSocket.connect((HOST, PORT))
    print("Connected to server!")

    #Takes filename
    filename = input("Enter the filename you want to download: ")
    #Encode it to binary and sends to server side
    clientSocket.send(filename.encode())

    #Determines wheather file exists or not
    response = clientSocket.recv(1024).decode()

    if response == "OK":
        print("Server found the file! Starting download...")

        file_size = int(clientSocket.recv(1024).decode())
        print(f"File size: {file_size} bytes")

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
                    print(f"Downloading... {progress:.1f}%", end="\r")

            print(f"\nDownload complete! File saved as '{new_filename}'")

        except IOError as e:
            print(f"File I/O error: {e}")

    else:
        print(f"Server says: {response}")

except socket.error as e:
    print(f"Connection error: {e}")
    print("Make sure the server is running before starting the client.")

finally:
    clientSocket.close()
    print("Connection closed.")