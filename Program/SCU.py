# SCU.py

import codecs
import math
import os
import random
import socket
import string
import sys
import time
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


# Delimiter for concatenating data
delimiter = ':-:'

# Data format used for IVs
dataType_IV = 'Binary'

# Block Padding
paddingChar = '0'

# High/Low
High = '1'
Low = '0'

# Set blocksizes
AES128BlockSize = 128
RSABlockSize = 4096

# Option bools
# Option = False


# Sets options
# def setOptions(options):
#     global option
#     option = options[0]


# Check the key size for selected algorithm
def checkKeySize(key, algorithm):

    # AES128
    if algorithm is 'AES128':
        if len(key) is not AES128BlockSize:
            print('AES128 key provided is not ' +  str(AES128BlockSize) + ' bits...')
            print('Length: ' + str(len(key)))
            return False

    # TODO Add RSA Key size check. Not certain how to gett size from PEM key formats
    return True


# Pads a data block with padding chars to beginning of string
def padBlock(data, blockSize):
    return data + (blockSize -len(data) % blockSize) * paddingChar


# Generate IV based on argument options
def generateIV(blockSize, encoding):

    # Binary IV of blockSize bits
    if encoding is 'Binary':
        return ''.join(str(random.randint(0, 1)) for i in range(blockSize))
    # Hex IV of blockSize hex characters
    if encoding is 'Hex':
        return ''.join(hex(random.randint(0, 16))[2:] for i in range(blockSize))
    # String IV of blockSize bytes
    if encoding is 'Bytes':
        return os.urandom(blockSize)


# Generate a random key string of specified length
def generateKey(bytes):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(bytes))


# Encrypt text
def encryptText(key, data, mode, algorithm):

    # Add the original message length to data to be encrypted
    data = delimiter.join((str(len(data)), data))

    # RSA
    if algorithm is 'RSA':
        # Returns tuple with [1] always empty
        cipher = RSA.importKey(key).encrypt(data.encode(), RSABlockSize)[0]
        return cipher

    # AES128
    if algorithm is 'AES128':
        # Cipher Block Chaining
        if mode is 'CBC':
            # Generate an initialization vector
            IV = generateIV(16, 'Bytes')

            # Pad the data to be a multiple of 16
            largestMultipleOf16 = (math.ceil(len(data)/16)*16)
            paddedData = str(padBlock(data, largestMultipleOf16)).encode()

            # Encrypt
            cipher = AES.new(key, AES.MODE_CBC, IV).encrypt(paddedData)

            return IV, cipher


# Decrypt text
def decryptText(key, cipher, mode, algorithm):

    # RSA
    if algorithm is 'RSA':
        plaintext = str(RSA.importKey(key).decrypt(cipher).decode())
        return plaintext

    # AES128
    if algorithm is 'AES128':
        # Cipher Block Chaining
        if mode is 'CBC':
            IV = cipher[0]
            data = cipher[1]
            plaintext = AES.new(key, AES.MODE_CBC, IV).decrypt(data)
            return plaintext


# TLSS/SL Summary
# 1. Client connects to server, shares certificate, asks server to identify itself
# 2.    Server sends certficate
# 3. Verify certificate against trusted certifcate authorities
#       - If enexpired, unrevoked, and common name is relevant for server
#           - Create, encrypt (with server public key), and send AES session key
# 4.    Server decrypts session key, send acknowlegement (encrypted with session key)
# .... All proceeding transmissions encrypted with session key


# Perform simplified TLS handshake as server
#   Returns secret AES session key negotiated
def serverSimpleTLSHandshake(serverPubKey, serverPrivateKey, socket):

    # Socket is pre-connected to client
    #   Listen for handshake start
    response = socket.recv(1024).decode()
    print('\t1)\tClient Handshake Request: ' + str(response))

    # Respond with real server public key
    message = serverPubKey

    # print('\tServer Public Key: ' + message)
    print('\t2)\tSending Server Public Key')
    socket.send(message.encode())

    # Listen for sessionKey (encrypted with serverPubKey)
    response = socket.recv(1024)
    print('\t3)\tReceived Encrypted Session Key')
    # print('\t\tEncrypted SessionKey: ' + str(codecs.encode(b'response', 'hex')))

    # Decrypt session key
    sessionKey = decryptText(serverPrivateKey, response, 'ECB', 'RSA')
    sessionKey = sessionKey.split(delimiter)[1]

    print('\t\tDecrypted SessionKey: ' + sessionKey)

    # Send ack encrypted with sessionKey
    ack = "TLS-SUCCESS"
    message = encryptText(sessionKey, ack, 'CBC', 'AES128')
    socket.send(message[0])
    socket.send(message[1])
    print('\t4)\tSending Server Encrypted Ack')
    print('\t\tServer Decrypted Ack: ' + ack)
    # print('\t\tServer Encrypted Ack: ' + str(message))

    # Return session key for securing session communications
    return sessionKey


# Perform simplified TLS handshake as client
#   Returns secret AES session key negotiated
def clientSimpleTLSHandshake(clientPubKey, socket):
    global keys

    # Socket is pre-connected to server
    print('\t1)\tStarting Simlple TLS Handshake')

    # Share the client public key and flag the start of handshake
    message = "TLS-START"
    socket.send(message.encode())

    # Listen for server's response containing real public key
    serverPubKey = socket.recv(1024).decode()
    print('\t2)\tGot Server Public Key')
    # print('\t\tServer Public Key: ' + str(serverPubKey))

    # No verification via certificate authorities in simple handshake

    # Generate session key and encrypt with server public key
    sessionKey = generateKey(int(AES128BlockSize/8))
    print('\t\tGenerated SessionKey: ' + str(sessionKey))

    # Encrypt and send sessionKey
    encryptedSessionKey = encryptText(serverPubKey, sessionKey, 'ECB', 'RSA')
    socket.send(encryptedSessionKey)
    print('\t3)\tSending Encrypted Session Key')
    # print('\t\tSessionKey Encryption Digest: ' + str(codecs.encode(b'encryptedSessionKey', 'hex')))

    # Await an acknowledgement encrypted with generated sessionKey
    response = [0, 0]
    response[0] = socket.recv(1024)
    response[1] = socket.recv(1024)

    # Decrypt response
    data = decryptText(sessionKey, response, 'CBC', 'AES128')
    ack = str(data.decode().split(':-:')[1].replace('0',''))
    print('\t4)\tServer Decrypted Ack: ' + ack)

    # Verify
    if 'TLS-SUCCESS' in ack:
        # Return session key for securing session communications
        return sessionKey
    else:
        # Kill the connection
        socket.close()

        return False
