# =============================================================================
# client.py
# CS310 - Computer Networks, Assignment 1
# File Transfer Client using TCP Socket Programming
# =============================================================================

import socket  # For creating and managing sockets
import os      # For file path operations

# ----------------------------- Configuration ---------------------------------
SERVER_IP   = "127.0.0.1"   # Server IP address (same machine for demo)
SERVER_PORT = 5000           # Must match the server's port
BUFFER_SIZE = 4096           # Number of bytes to receive per chunk
# -----------------------------------------------------------------------------


def download_file(filename):
    """
    Connects to the file server, requests the specified file,
    receives it with progress updates, and saves it locally.

    Args:
        filename (str): The name of the file to request from the server.
    """

    # Step 1: Create a TCP socket (SOCK_STREAM = TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Step 2: Connect to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"[CLIENT] Connected to server at {SERVER_IP}:{SERVER_PORT}")

        # Step 3: Send the requested filename to the server
        client_socket.send(filename.encode())
        print(f"[CLIENT] Requested file: '{filename}'")

        # Step 4: Wait for the server's response (ACK or error)
        response = client_socket.recv(BUFFER_SIZE).decode()

        # Step 5: Handle server response
        if response == "File does not exist":
            # Server could not find the file
            print(f"[CLIENT] ERROR: {response}")
            return

        if not response.startswith("ACK"):
            # Unexpected response from server
            print(f"[CLIENT] ERROR: Unexpected server response: {response}")
            return

        # Parse the file size from the ACK message (format: "ACK <file_size>")
        file_size = int(response.split()[1])
        print(f"[CLIENT] Server acknowledged. File size: {file_size} bytes.")
        print(f"[CLIENT] Starting download...")

        # Step 6: Receive the file in chunks and save it locally
        bytes_received = 0
        last_reported  = -1   # Tracks the last printed percentage (avoids repeats)

        # Save file with "_downloaded" suffix to distinguish from originals
        save_name = os.path.splitext(filename)[0] + "_downloaded" + os.path.splitext(filename)[1]

        with open(save_name, "wb") as f:
            while bytes_received < file_size:
                # Calculate how much data is still needed
                remaining = file_size - bytes_received
                chunk = client_socket.recv(min(BUFFER_SIZE, remaining))

                if not chunk:
                    # Connection closed before transfer was complete
                    print("\n[CLIENT] ERROR: Connection lost during transfer.")
                    break

                f.write(chunk)            # Write chunk to file
                bytes_received += len(chunk)

                # Step 7: Calculate and display download progress percentage
                percent = int((bytes_received / file_size) * 100)

                # Only print when percentage changes (avoids flooding console)
                if percent != last_reported:
                    print(f"[CLIENT] Downloading... {percent}%")
                    last_reported = percent

        # Step 8: Confirm successful download
        if bytes_received == file_size:
            print(f"[CLIENT] Download complete! File saved as '{save_name}'.")
        else:
            print(f"[CLIENT] WARNING: Expected {file_size} bytes, received {bytes_received} bytes.")

    except ConnectionRefusedError:
        # Server is not running or port is wrong
        print(f"[CLIENT] ERROR: Could not connect to server at {SERVER_IP}:{SERVER_PORT}.")
        print("[CLIENT] Make sure the server is running first.")

    except OSError as e:
        # Handle file I/O or socket errors
        print(f"[CLIENT] ERROR: {e}")

    finally:
        # Step 9: Close the socket cleanly
        client_socket.close()
        print("[CLIENT] Connection closed.")


# Entry point — prompt user for filename
if __name__ == "__main__":
    filename = input("Enter the filename to download: ").strip()

    if not filename:
        print("[CLIENT] ERROR: No filename entered.")
    else:
        download_file(filename)
