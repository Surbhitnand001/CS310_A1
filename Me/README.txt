CS310 Assignment 1 - File Transfer Application
Student Name: Surbhit Nand(S11230283)
Student Name: Parvish Mohan(S11230414)

Overview
This project is a simple client-server file transfer application built with Python socket programming.
It uses TCP, runs on the same PC for demonstration, and supports downloading a file from the server to the client.

How It Works
1. The server starts first and listens on 127.0.0.1:5000.
2. The client connects to the server and sends the name of the file it wants.
3. The server checks whether the file exists.
4. If the file exists, the server sends the file size and then the file contents.
5. The client receives the file, shows download progress, and saves it in the current working directory with a _downloaded suffix.

Requirements Covered
1. Python 3 is used.
2. TCP is used as the reliable transport protocol.
3. The server and client both use 127.0.0.1 and port 5000.
4. The server handles one client connection at a time.
5. Error handling is included for connection and file transfer problems.
6. The code is commented to show the flow of connection, file request, transfer, and progress reporting.

Run Instructions
1. Place a sample file such as test.txt in the server folder.
2. Open a terminal in the folder that contains fileserver.py and client.py.
3. Start the server:
	python fileserver.py
4. Open a second terminal in the same folder.
5. Start the client:
	python client.py
6. When prompted, type the name of the file to download, for example:
	test.txt

Expected Result
The client downloads the file and saves it locally with a name such as test_downloaded.txt.