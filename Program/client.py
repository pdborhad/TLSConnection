# client.py this file is responsible for sending data to server 

import os
import random 
import socket
import sys
import time
from threading import Thread

import SCU

# Delimiter for concatenating data
delimiter = ':-:'

# Reads the data line from a file
def readData(afile):
	for num, aline in enumerate(afile):
		return aline


# Creates a new client and connects to the server
def createClientConnection(ID, serverAddress):
	print('Starting a new client: ' + ID)
	
	# Set up client
	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.connect(serverAddress)
	
	# Do TLS handshake
	sessionKey = SCU.clientSimpleTLSHandshake(clientPubKey, connection)
	
	# Pick something to send
	
	message = readData(open('./receicedData/receivedMessage.txt')).strip('\n')
	print('\n\t' + ID + ' Message: ' + message)
	
	# Delete the readFile.txt from the location so arduino can creare again. 
	#print('\n Removing the readFile.txt from location... ')
	#os.remove('./readFile.txt')
	
	# Returns IV, Cipher
	IV, cipher = SCU.encryptText(sessionKey, message, 'CBC', 'AES128')
	
	connection.send(IV)
	connection.send(cipher)
	
	
	# Wait for an encrypted Acknoledgment
	#   IV is sent first, ciphertext follows after
	response = [0, 0]
	response[0] = connection.recv(1024)
	response[1] = connection.recv(1024)
	
	
	# Decrypt response
    #   Returns: Length:-:Plaintext+PaddingChars
	data = SCU.decryptText(sessionKey, response, 'CBC', 'AES128')
	# Report echo with length and padding characters removed
	plaintext = data.decode().split(delimiter)[1].replace('0','')
	print('\t******** Replay from the server : ' + plaintext)
	
	# Close
	connection.close()
	
#----- Main -----#
# Check arguments
if len(sys.argv) < 3:
    print('Usage: python client.py HOST PORT')
    sys.exit(1)

dir = os.path.dirname(sys.argv[0])
if dir == '':
    dir = os.curdir

# Get RSA Keys
with open('ClientKeys/Client.pubkey', 'r') as pubKeyFile:
    clientPubKey = pubKeyFile.read()
with open('ClientKeys/Client.pkey', 'r') as privKeyFile:
    clientPrivKey = privKeyFile.read()

	
i = 0
while True:
	ID = 'Client' + str(i)
	t = Thread(target=createClientConnection, args=(ID, (sys.argv[1], int(sys.argv[2]))))
	t.start()
	i += 1
	time.sleep(10)