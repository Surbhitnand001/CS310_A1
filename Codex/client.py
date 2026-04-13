"""
CS310 Assignment 1 - File Transfer Client
Student Name: [Add Your Name Here]

This client connects to 127.0.0.1:5000, requests a file by name, receives the
server response, shows the download progress percentage, and saves the file in
the current working directory with a "_downloaded" suffix.
"""

import os
import socket


HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 4096


def receive_header(sock):
    """Receive the one-line header sent by the server."""
    header_bytes = b""
    while b"\n" not in header_bytes:
        chunk = sock.recv(1)
        if not chunk:
            raise ConnectionError("Connection closed before header was received.")
        header_bytes += chunk
    return header_bytes.decode("utf-8").strip()


def build_output_filename(filename):
    """Save the incoming file with a _downloaded suffix."""
    name, extension = os.path.splitext(filename)
    return f"{name}_downloaded{extension}"


def download_file(filename):
    """Connect to the server, request a file, and save it locally."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        client_socket.sendall(filename.encode("utf-8"))
        print(f"Requested file: {filename}")

        header = receive_header(client_socket)
        parts = header.split("|", 1)

        if parts[0] == "ERROR":
            message = parts[1] if len(parts) > 1 else "Unknown server error"
            print(message)
            return

        if parts[0] != "OK" or len(parts) != 2:
            print("Received an invalid response from the server.")
            return

        total_size = int(parts[1])
        output_filename = build_output_filename(filename)
        received_bytes = 0
        last_reported_percentage = -1

        with open(output_filename, "wb") as file_handle:
            while received_bytes < total_size:
                chunk = client_socket.recv(min(BUFFER_SIZE, total_size - received_bytes))
                if not chunk:
                    raise ConnectionError("Connection lost during file transfer.")

                file_handle.write(chunk)
                received_bytes += len(chunk)

                percentage = int((received_bytes / total_size) * 100) if total_size else 100
                if percentage != last_reported_percentage:
                    print(f"Downloading... {percentage}%")
                    last_reported_percentage = percentage

        print(f"Download complete. File saved as: {output_filename}")
        print("File transfer successful.")


if __name__ == "__main__":
    requested_filename = input("Enter the name of the file to download: ").strip()

    if not requested_filename:
        print("Please enter a valid filename.")
    else:
        try:
            download_file(requested_filename)
        except ConnectionRefusedError:
            print("Could not connect to the server. Make sure the server is running first.")
        except FileNotFoundError:
            print("Unable to create the output file in the current directory.")
        except OSError as error:
            print(f"Network or file error: {error}")
