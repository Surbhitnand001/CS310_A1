"""
CS310 - Computer Networks, Assignment 1 (Semester 1, 2026)
File Transfer Server using TCP Socket Programming

Authors:
    Surbhit Nand   - S11230283
    Parvish Mohan  - S11230414

This server listens on 127.0.0.1:5000, accepts a single client connection,
receives a filename request, and transmits the file in chunks if it exists
in the server's working directory.

Protocol:
    Success header : "OK|<file_size>\n"
    Error header   : "ERROR|<message>\n"
"""

import os
import socket

# ----------------------------- Configuration ---------------------------------
HOST = "127.0.0.1"   # Loopback IP address (same machine for demo)
PORT = 5000          # Port number (above 1024, as required)
BUFFER_SIZE = 4096   # Chunk size in bytes for transfer
# -----------------------------------------------------------------------------


def send_line(connection, message):
    """Send a single newline-terminated text message to the client."""
    connection.sendall(f"{message}\n".encode("utf-8"))


def send_error(connection, message):
    """Send an error response to the client."""
    send_line(connection, f"ERROR|{message}")


def send_file(connection, filename):
    """Send a success header followed by the file bytes in chunks."""
    file_size = os.path.getsize(filename)
    send_line(connection, f"OK|{file_size}")
    print(f"[SERVER] File found. Size: {file_size} bytes. Sending...")

    bytes_sent = 0
    last_reported = -1
    with open(filename, "rb") as file_handle:
        while True:
            chunk = file_handle.read(BUFFER_SIZE)
            if not chunk:
                break
            connection.sendall(chunk)
            bytes_sent += len(chunk)

            # Print progress only when the percentage changes
            percent = int((bytes_sent / file_size) * 100)
            if percent != last_reported:
                print(f"[SERVER] Uploading... {percent}%")
                last_reported = percent

    print(f"[SERVER] File transfer successful. {bytes_sent} bytes sent.")


def start_server():
    """Create the listening socket, accept one client, and handle one request."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow the port to be reused immediately after the server stops
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[SERVER] Listening on {HOST}:{PORT}")
        print("[SERVER] Waiting for a connection...")

        client_socket, client_address = server_socket.accept()
        print(f"[SERVER] Client connected from {client_address}")
        print("[SERVER] Ready for communication.")

        try:
            # Receive the requested filename from the client
            filename = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()
            print(f"[SERVER] Client requested file: '{filename}'")

            if not filename:
                send_error(client_socket, "No filename provided")
                return

            if not os.path.isfile(filename):
                error_message = "File does not exist"
                print(f"[SERVER] File '{filename}' not found. Notifying client.")
                send_error(client_socket, error_message)
                return

            send_file(client_socket, filename)

        except ConnectionResetError:
            print("[SERVER] ERROR: Client disconnected unexpectedly.")
        except OSError as e:
            print(f"[SERVER] ERROR reading file: {e}")
            try:
                send_error(client_socket, "Server encountered an error")
            except OSError:
                pass
        finally:
            client_socket.close()
            print("[SERVER] Client connection closed.")

    except socket.error as e:
        print(f"[SERVER] Socket error: {e}")
    finally:
        server_socket.close()
        print("[SERVER] Server closed.")


# Entry point
if __name__ == "__main__":
    start_server()
