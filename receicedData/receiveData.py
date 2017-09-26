#! /usr/bin/python
import serial
import time
import sys
import os
import os.path

print('\n The terminal selected is -- ', str(sys.argv[1]))

if str(sys.argv[1]) is None:
	print('\n You are passing nothing to this script')
else :
	ser = serial.Serial(sys.argv[1], 9600)
	while 1:
		"""
		print('\n $$$$$ Reading Data $$$$$...')
		surgeNumber=ser.readline()
		print('\n surgeNumber is : ', surgeNumber )
		
		elapsTime=ser.readline()
		print('\n elapsTime is : ', elapsTime)
		
		timeDone = ser.readline()
		print('\n timeDone is : ', timeDone)
		
		flowRate = ser.readline()
		print('\n flowRate is : ', flowRate)
		
		appDepth = ser.readline()
		print('\n appDepth is : ', appDepth)
		
		waterAmount = ser.readline()
		print('\n waterAmount is : ', waterAmount)
		"""
		print('\n $$$$$ Reading Data $$$$$...')
		dataReceived=ser.readline()
		dataReceived = dataReceived.decode('utf8')
		strdataReceived = dataReceived.replace('\r', '')
		print('\n Data received is : ', strdataReceived)
		
		if os.path.isfile('receivedMessage.txt'):
			print('\n file alredy exist. Deleting it ...')
			os.remove('receivedMessage.txt')
			print('\n File deleted. Ceating new and updating data...')
			try:
				print('\n Creating file....')
				file=open('receivedMessage.txt','w')
				print('\n file created')
				#writeMessage = str(surgeNumber)+'/' + str(elapsTime) + '/'+ str(timeDone) + '/' + str(flowRate) + '/' + str(appDepth) + '/' + str(waterAmount) + '\n'
				#print('\n Message is : ', writeMessage)
				#file.write(writeMessage)
				file.write(strdataReceived)
				file.close()
				print('\n @@@@@ Transaction Done @@@@@@')
			except:
				print("error occured")
				sys.exit(0)
		time.sleep(2)
