# =============================================================================
# fileserver.py
# CS310 - Computer Networks, Assignment 1
# File Transfer Server using TCP Socket Programming
# =============================================================================

import socket  # For creating and managing sockets
import os      # For checking file existence and getting file size

# ----------------------------- Configuration ---------------------------------
SERVER_IP   = "127.0.0.1"   # Localhost IP address (loopback)
SERVER_PORT = 5000           # Port number (above 1024, as required)
BUFFER_SIZE = 4096           # Number of bytes to send per chunk
# -----------------------------------------------------------------------------


def start_server():
    """
    Creates a TCP server socket, waits for a client connection,
    handles a file request, and sends the file if it exists.
    """

    # Step 1: Create a TCP socket (SOCK_STREAM = TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow the port to be reused immediately after the server stops
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Step 2: Bind the socket to the server IP and port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Step 3: Start listening for incoming connections (max 1 queued connection)
    server_socket.listen(1)
    print(f"[SERVER] Listening on {SERVER_IP}:{SERVER_PORT} ...")

    # Step 4: Accept a client connection (blocks here until client connects)
    client_socket, client_address = server_socket.accept()
    print(f"[SERVER] Client connected from {client_address}")
    print("[SERVER] Ready for communication.")

    try:
        # Step 5: Receive the requested filename from the client
        filename = client_socket.recv(BUFFER_SIZE).decode()
        print(f"[SERVER] Client requested file: '{filename}'")

        # Step 6: Check if the file exists in the server's working directory
        if not os.path.exists(filename):
            # File does not exist — send error message to client
            client_socket.send("File does not exist".encode())
            print(f"[SERVER] File '{filename}' not found. Error sent to client.")
        else:
            # File exists — send positive acknowledgement to client
            file_size = os.path.getsize(filename)
            # Send ACK along with file size so client can track progress
            ack_message = f"ACK {file_size}"
            client_socket.send(ack_message.encode())
            print(f"[SERVER] File found. Size: {file_size} bytes. Sending...")

            # Step 7: Open and send the file in chunks
            bytes_sent = 0
            with open(filename, "rb") as f:
                while True:
                    chunk = f.read(BUFFER_SIZE)  # Read one chunk at a time
                    if not chunk:
                        break  # End of file reached
                    client_socket.sendall(chunk)  # Send chunk reliably
                    bytes_sent += len(chunk)

            print(f"[SERVER] File transfer successful. {bytes_sent} bytes sent.")
            print("[SERVER] File transfer complete.")

    except ConnectionResetError:
        # Handle unexpected client disconnection
        print("[SERVER] ERROR: Client disconnected unexpectedly.")

    except OSError as e:
        # Handle file I/O errors
        print(f"[SERVER] ERROR reading file: {e}")

    finally:
        # Step 8: Close both sockets cleanly
        client_socket.close()
        server_socket.close()
        print("[SERVER] Connection closed.")


# Entry point
if __name__ == "__main__":
    start_server()
