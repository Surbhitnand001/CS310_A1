"""
CS310 Assignment 1 - File Transfer Server
Student Name: [Add Your Name Here]

This server listens on 127.0.0.1:5000, receives a file request from one client,
checks whether the file exists in the current working directory, and sends the
file to the client if available.
"""

import os
import socket


HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 4096


def receive_requested_filename(connection):
    """Read the requested filename sent by the client."""
    data = connection.recv(BUFFER_SIZE)
    if not data:
        raise ConnectionError("No file request was received from the client.")
    return data.decode("utf-8").strip()


def send_error(connection, message):
    """Send an error response to the client."""
    connection.sendall(f"ERROR|{message}\n".encode("utf-8"))


def send_file(connection, filename):
    """Send a success header followed by the file bytes."""
    file_size = os.path.getsize(filename)
    connection.sendall(f"OK|{file_size}\n".encode("utf-8"))

    sent_bytes = 0
    with open(filename, "rb") as file_handle:
        while True:
            chunk = file_handle.read(BUFFER_SIZE)
            if not chunk:
                break
            connection.sendall(chunk)
            sent_bytes += len(chunk)

    print(f"File transfer successful. Sent {sent_bytes} bytes.")


def start_server():
    """Create the socket, wait for one client, and process one request."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        print(f"Server is listening on {HOST}:{PORT}")
        print("Waiting for a client to connect...")

        connection, address = server_socket.accept()
        with connection:
            print(f"Connected to client at {address}")
            print("Server is ready for communication.")

            try:
                requested_file = receive_requested_filename(connection)
                print(f"Client requested file: {requested_file}")

                if not os.path.isfile(requested_file):
                    error_message = "File does not exist"
                    print(error_message)
                    send_error(connection, error_message)
                    return

                print("File found. Permission granted. Starting file transfer...")
                send_file(connection, requested_file)
                print("Download complete.")

            except OSError as error:
                print(f"File or socket error: {error}")
                try:
                    send_error(connection, "Server encountered an error")
                except OSError:
                    pass
            except ConnectionError as error:
                print(f"Connection error: {error}")


if __name__ == "__main__":
    start_server()
