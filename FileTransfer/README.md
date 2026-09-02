# CS310 - Computer Networks

## Assignment 1: File Transfer Application

**Semester I, 2026**

---

## Authors

- **Surbhit Nand** — Student ID: S11230283
- **Parvish Mohan** — Student ID: S11230414

---

## Overview

This project implements a simple TCP-based file transfer system consisting of two Python programs:

- **`fileserver.py`** — A server that listens for client connections, validates file requests, and transmits files.
- **`client.py`** — A client that connects to the server, requests a file, receives it with progress updates, and saves it locally.

The application demonstrates core socket programming concepts including TCP connection establishment, reliable data transfer, error handling, and progress monitoring.

---

## Files Included

| File            | Description                          |
| --------------- | ------------------------------------ |
| `fileserver.py` | TCP file transfer server             |
| `client.py`     | TCP file transfer client             |
| `README.md`     | This documentation file              |
| `test.txt`      | Sample file for testing the transfer |

---

## Requirements

- Python 3.x (no external libraries required — uses built-in `socket` and `os` modules only)
- Two terminal windows (both on the same machine for demonstration)

---

## How to Run

### Step 1 — Place a test file in the server's folder

Copy any file (e.g., `test.txt`, an image, or a video) into the same directory as `fileserver.py`.

### Step 2 — Start the server

Open a terminal in the project folder and run:

```bash
python fileserver.py
```

You should see:

```
[SERVER] Listening on 127.0.0.1:5000
[SERVER] Waiting for a connection...
```

### Step 3 — Start the client

Open a **second terminal** in the same directory and run:

```bash
python client.py
```

You will be prompted:

```
Enter the filename to download:
```

Type the name of a file that exists in the server's folder (e.g., `test.txt`) and press Enter.

### Step 4 — Observe output

**Server terminal** will show:

```
[SERVER] Client connected from ('127.0.0.1', XXXXX)
[SERVER] Ready for communication.
[SERVER] Client requested file: 'test.txt'
[SERVER] File found. Size: XXXX bytes. Sending...
[SERVER] Uploading... 10%
[SERVER] Uploading... 25%
...
[SERVER] Uploading... 100%
[SERVER] File transfer successful. XXXX bytes sent.
[SERVER] Client connection closed.
[SERVER] Server closed.
```

**Client terminal** will show:

```
[CLIENT] Connected to server at 127.0.0.1:5000
[CLIENT] Requested file: 'test.txt'
[CLIENT] Server acknowledged. File size: XXXX bytes.
[CLIENT] Starting download...
[CLIENT] Downloading... 10%
[CLIENT] Downloading... 25%
...
[CLIENT] Downloading... 100%
[CLIENT] Download complete! File saved as 'test_downloaded.txt'.
[CLIENT] Connection closed.
```

---

## Protocol

The client and server communicate using a simple line-delimited text protocol:

| Situation      | Server sends                   |
| -------------- | ------------------------------ |
| File found     | `OK\|<file_size>\n`            |
| File not found | `ERROR\|File does not exist\n` |
| Other error    | `ERROR\|<message>\n`           |

After sending `OK|<size>`, the server streams the raw file bytes. The client reads exactly `<file_size>` bytes and writes them to disk.

---

## Error Handling

| Scenario                      | Behaviour                                                    |
| ----------------------------- | ------------------------------------------------------------ |
| File does not exist on server | Server sends `ERROR\|File does not exist`; client prints it  |
| Server not running            | Client prints connection refused error and exits cleanly     |
| Connection lost mid-transfer  | Client detects incomplete transfer and prints a warning      |
| Empty filename                | Server sends `ERROR\|No filename provided`                   |
| File read/write errors        | Both programs catch `OSError` and print a meaningful message |

---

## Configuration

Both files use the following constants (defined at the top of each file):

| Constant      | Value       | Description                        |
| ------------- | ----------- | ---------------------------------- |
| `HOST`        | `127.0.0.1` | Localhost (loopback) IP address    |
| `PORT`        | `5000`      | Port number used for communication |
| `BUFFER_SIZE` | `4096`      | Chunk size in bytes for transfer   |

---

## Output File

The downloaded file is saved in the client's working directory with a `_downloaded` suffix:

- `test.txt` → `test_downloaded.txt`
- `image.jpg` → `image_downloaded.jpg`
- `video.mp4` → `video_downloaded.mp4`

---

## Notes

- The server handles **one client at a time** (no multithreading), as per the assignment requirements.
- TCP is used as the transport protocol to ensure reliable, ordered data delivery.
- All code is commented to clearly explain socket creation, connection, file request, data transfer, and progress reporting.
- The implementation works for any file type (text, images, video, etc.) because data is transferred as raw bytes.
