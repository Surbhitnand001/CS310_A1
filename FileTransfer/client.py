"""
CS310 - Computer Networks, Assignment 1 (Semester 1, 2026)
File Transfer Client using TCP Socket Programming

Authors:
    Surbhit Nand   - S11230283
    Parvish Mohan  - S11230414

This client connects to 127.0.0.1:5000, requests a file by name, receives the
server response, displays the download progress percentage, and saves the file
in the client's working directory with a "_downloaded" suffix.

Protocol:
    Success header : "OK|<file_size>\n"
    Error header   : "ERROR|<message>\n"
"""

import os
import socket

# ----------------------------- Configuration ---------------------------------
HOST = "127.0.0.1"   # Server IP address (same machine for demo)
PORT = 5000          # Must match the server's port
BUFFER_SIZE = 4096   # Chunk size in bytes for transfer
# -----------------------------------------------------------------------------


def receive_header(connection):
    """Receive the one-line header sent by the server (terminated by '\\n')."""
    header_bytes = b""
    while b"\n" not in header_bytes:
        chunk = connection.recv(1)
        if not chunk:
            raise ConnectionError("Connection closed before header was received.")
        header_bytes += chunk
    return header_bytes.decode("utf-8").strip()


def build_output_filename(filename):
    """Return the local filename with a '_downloaded' suffix."""
    name, extension = os.path.splitext(filename)
    return f"{name}_downloaded{extension}"


def download_file(filename):
    """Connect to the server, request a file, and save it locally."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print(f"[CLIENT] Connected to server at {HOST}:{PORT}")

        # Send the requested filename to the server
        client_socket.sendall(filename.encode("utf-8"))
        print(f"[CLIENT] Requested file: '{filename}'")

        # Read the server's response header
        header = receive_header(client_socket)
        parts = header.split("|", 1)

        if parts[0] == "ERROR":
            message = parts[1] if len(parts) > 1 else "Unknown server error"
            print(f"[CLIENT] ERROR: {message}")
            return

        if parts[0] != "OK" or len(parts) != 2:
            print(f"[CLIENT] ERROR: Unexpected server response: {header}")
            return

        # Parse the file size from the OK header (format: "OK|<file_size>")
        file_size = int(parts[1])
        print(f"[CLIENT] Server acknowledged. File size: {file_size} bytes.")
        print("[CLIENT] Starting download...")

        save_name = build_output_filename(filename)
        bytes_received = 0
        last_reported = -1

        with open(save_name, "wb") as file_handle:
            while bytes_received < file_size:
                remaining = file_size - bytes_received
                chunk = client_socket.recv(min(BUFFER_SIZE, remaining))

                if not chunk:
                    print("\n[CLIENT] ERROR: Connection lost during transfer.")
                    break

                file_handle.write(chunk)
                bytes_received += len(chunk)

                # Print progress only when the percentage changes
                percent = int((bytes_received / file_size) * 100)
                if percent != last_reported:
                    print(f"[CLIENT] Downloading... {percent}%")
                    last_reported = percent

        if bytes_received == file_size:
            print(f"[CLIENT] Download complete! File saved as '{save_name}'.")
        else:
            print(f"[CLIENT] WARNING: Expected {file_size} bytes, "
                  f"received {bytes_received} bytes.")

    except ConnectionRefusedError:
        print(f"[CLIENT] ERROR: Could not connect to server at {HOST}:{PORT}.")
        print("[CLIENT] Make sure the server is running first.")
    except ConnectionError as e:
        print(f"[CLIENT] ERROR: {e}")
    except OSError as e:
        print(f"[CLIENT] ERROR: {e}")
    finally:
        client_socket.close()
        print("[CLIENT] Connection closed.")


# Entry point — prompt user for filename
if __name__ == "__main__":
    filename = input("Enter the filename to download: ").strip()

    if not filename:
        print("[CLIENT] ERROR: No filename entered.")
    else:
        download_file(filename)
