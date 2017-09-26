# Simple TLS connection.

#Receive Data from microcontroller over serial communication and send it to remote device over internet on TLS connection. 

/*

This project is built to send the data from Microcontrller to remote desktop over the internet.
Microcontrtoller sends the data to RasPi over serial communication. RasPi create a SSL connection to remote device and send the data to remote desktop. This project is run on a single machine which works as both the server and the client. The microcontroler used for sending data to RasPi is ArduinoDue board.

*/

###  How to run the project.

Before start the server and client, write a code to send a data from arduino to RasPi over serial commuincation. The folder 'receicedData' above has 'startReceiver' script which constantly receives the data from Arduino board on serial-0-interface and saves to the file 'receicedData/receivedMessage.txt'. Make sure you get the data to this file before starting the server and client. Once you confirmed, perform next steps. 

Step-1: Run following file 
./setup

The setup will create the public and private keys for server and client. These keys are required for SSL connection.

Step-1: start server
./startServer

This file internally calls a Python script 'server.py' and listens connections on port 8000. If it listens any connection on the port, it accepts the message and saves into './receivedMessage.txt' file.

Step-3: start client
./startClient

This file starts client machine. It calls 'client.py' and create secure connection to server. Once the cilent connects to the server, it send a data to the server. The data to be sent is saved in './receicedData/receivedMessage.txt'
