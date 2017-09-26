# Server.py
# This file is responsible to work on client connection and send and receive the data from client such as irrigation time, time remaining, flowrate, amount of water supplied. 

import os
import select
import socket
import sys

import SCU


#Buffers 
# Key:connection object
clients = {}				#Client Socket address
sessionKeys = {}			#Client session keys.

#HOST  = 					#Host IP Address

# Removing client from buffers
def dropClient(connection, errors=None):
    if errors:
        print('Client %s left unexpectedly:' % (clients[connection],))
        print('  \n', errors)
    else:
        print('Client %s left politely\n' % (clients[connection],))
    del clients[connection]
    connection.close()
	

# Processes the data sent from clients
def processData(data, sessionKey):
	print('Processing Data\n')
	#Decrypt the Data
	response = SCU.decryptText(sessionKey, data, 'CBC', 'AES128')
	# Determine plaintext from response with length and padding character removed
	plaintext = response.decode().split(':-:')[1].replace('0', '')
	print('\n\t PlainText: ' + str(plaintext))
	if plaintext != '' :
		ackMessage = "ack"
		with open('receivedMessage.txt', 'w') as writeText:
			writeText.write(plaintext)
			writeText.write('\n')
		return SCU.encryptText(sessionKey, ackMessage, 'CBC', 'AES128')

	# Encrypt data for echo
    #   Returns: IV, cipher
    #return SCU.encryptText(sessionKey, plaintext, 'CBC', 'AES128')
	
	
#----- Main Program -----#
if len(sys.argv) < 2 or sys.argv[1] == '-h':
    print('Usage: python3 server.py PORT [options]')
    print(' Options:')
    print('\t-h                  Display this menu')
    sys.exit(1)

	
print('\n\nStarting Simple TLS Echo Server on port ' + sys.argv[1] + '...\n')

# Set directory to script location
dir = os.path.dirname(sys.argv[0])
print('directory is ' + dir + '\n')

if dir == '':
    dir = os.curdir

# Get RSA Keys
with open('ServerKeys/Server.pubkey', 'r') as pubKeyFile:
	serverPubKey = pubKeyFile.read()
with open('ServerKeys/Server.pkey', 'r') as privKeyFile:
	serverPrivKey = privKeyFile.read()
	
# Set up TCP/IP  echo server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', int(sys.argv[1])))
server.listen(5)

# Run until stopped
while True:
	#wait for a connection
	print('Waiting for a connection ... ')
	connection, client_address = server.accept()
	clients[connection] = client_address
	
	try:
		print('\nConnection From: ' + str(client_address))
		
		#Do TLS Handshek to get sessionKey
		sessionKeys[connection] = SCU.serverSimpleTLSHandshake(serverPubKey, serverPrivKey, connection)
		
		# Listen for encrypted message
		data = [0, 0]
		data[0] = connection.recv(1024)
		data[1] = connection.recv(1024)
	
		# Process and send encrypted echo
		if data[0] and data[1]:
			IV, encryptedEcho = processData(data, sessionKeys[connection])
			connection.send(IV)
			connection.send(encryptedEcho)
		else:
			break
			
	finally:
		#CleanUp the connection
		dropClient(connection)