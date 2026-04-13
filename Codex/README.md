# CS310 Assignment 1 - File Transfer Application

Student Name: [Add Your Name Here]  
Student ID: [Add Your Student ID Here]

## Overview

This assignment implements a simple file transfer application using Python socket
programming and TCP. The server waits for a client request, checks if the
requested file exists, and sends the file to the client. The client receives
the file, displays the download progress in percentage form, and saves the file
locally with a `_downloaded` suffix.

## Files

- `fileserver.py`: Starts the server, validates the requested file, and sends
  the file to the client.
- `client.py`: Connects to the server, requests a file, displays progress, and
  saves the downloaded file.

## Features

- Uses TCP for reliable transfer.
- Hard-coded server settings:
  - IP address: `127.0.0.1`
  - Port: `5000`
- Handles one client at a time.
- Sends a clear error message if the requested file does not exist.
- Displays progress updates such as `Downloading... 45%`.
- Prints success messages after the transfer finishes.

## How It Works

1. Run `fileserver.py` first.
2. The server listens on `127.0.0.1:5000`.
3. Run `client.py` in a different terminal.
4. Enter the filename to download when prompted.
5. The client sends the filename to the server.
6. The server checks whether the file exists in its current folder.
7. If the file exists:
   - The server sends `OK|file_size`
   - The server sends the file contents
8. If the file does not exist:
   - The server sends `ERROR|File does not exist`
9. The client shows the download progress and saves the file locally.

## How to Run

Open two terminals in the folder containing the program files.

### Terminal 1 - Start the server

```powershell
python fileserver.py
```

### Terminal 2 - Start the client

```powershell
python client.py
```

When prompted, type the name of the file that exists in the server folder, for
example:

```text
test.txt
```

## Testing Notes

- Place a sample file such as `test.txt` or `image.jpg` in the same directory as
  `fileserver.py` before starting the server.
- After the transfer, the client will save the file as:
  - `test_downloaded.txt`
  - `image_downloaded.jpg`

## Error Handling

- If the server is not running, the client shows a connection error.
- If the file does not exist, the client shows `File does not exist`.
- If the connection breaks during transfer, the client shows an error message.

## Submission Notes

- Rename the main submission folder to:
  `YourName_StudentID_FileTransfer_Assignment`
- Include this README and both Python files inside that folder.
- Replace the placeholder name and ID in this README and in both Python files
  before submission.
