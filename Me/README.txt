# Socket programming
## CS310 ASSIGNMNET 1 - SEMESTER 1

Authors : Surbhit Nand  - S11230283
		: Parvish Mohan - S11230414

## Overview
This appliication illustrates a simple file transfer protocol(FTP) using the Transfer Conbtrol Protocol(TCP) socket avaiable through the library of Python.
It consists of two programs, the cilent & server that will be run on the same machine on separate windows terminal. Ther server will listen for any client connection,
validates wheather the requested files exists or not and transmit the file. The client connects to the server than requests a file of any type, displays the download progress and 
saves the file locally with a "_downloaded" suffix added to its end. 

## Files included
'fileserver.py' -> server program that handles the files request and transfers
'client.py'     -> client program which handles the request and receives the files
'README.txt'    -> this file

## How to Run

### STEP 1 - Placement of the files
Place the 'client.py', 'fileserver.py' and the file you wish to send e.g. test.txt, by the server and be receveied 
by the client in the same folder

### STEP 2 - Start the server 
Open the terminal and naviagte to where you have stored all the above mentioned files
than type 'python fileserver.py'
You will see -> Sever is waiting for a connection

### STEP 3 - Start the client
Open termainal and naviagte to the folder
than type 'python client.py'

### STEP 4 - Enter File name
After you have run 'python client.py'
You will see a prompt to enter the file name where you will type the
<filename>.<filetype>
E.g. test.txt

### STEP 5 - Display the download progression
The client side will display the download progress
Upon showing Downlaoding ...100%
The file has downloaded and is saved as <filename>_downloaded.txt
E.g. test.txt -> file requested by the client
	 test_downloaded.txt -> downloaded version on the client side
