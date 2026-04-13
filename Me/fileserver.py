# Authors: Surbhit Nand(S11230283), Parvish Mohan(S11230414)

import socket
import os

HOST = "127.0.0.1"  
PORT = 5000          

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    serverSocket.bind((HOST, PORT))

    serverSocket.listen(1)
    print("Server is waiting for a connection...")

    clientSocket, client_address = serverSocket.accept()
    print(f"Connected to {client_address}. Ready for communication.")

    filename = clientSocket.recv(1024).decode()
    print(f"Client requested file: {filename}")

    if os.path.exists(filename):
        clientSocket.send("OK".encode())
        print(f"File '{filename}' found. Sending...")

        file_size = os.path.getsize(filename)
        clientSocket.send(str(file_size).encode())

        try:
            with open(filename, "rb") as f:
                bytes_sent = 0
                while True:
                    chunk = f.read(1024)

                    if not chunk:
                        break

                    clientSocket.send(chunk)
                    bytes_sent += len(chunk)

            print("File transfer successful")

        except IOError as e:
            print(f"File I/O error: {e}")

    else:
        clientSocket.send("File does not exist".encode())
        print("File not found. Notifying client.")

except socket.error as e:
    print(f"Socket error: {e}")

finally:
    try:
        clientSocket.close()
    except:
        pass
    serverSocket.close()
    print("Server closed.")