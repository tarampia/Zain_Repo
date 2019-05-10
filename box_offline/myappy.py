#!/usr/bin/env python


import time
import serial
#import json 
import json
import uuid
from uuid import UUID  
import requests
#import urllib.parse
import datetime
import Adafruit_DHT
import sqlite3
from picamera import PiCamera
from time import sleep
import os
from subprocess import call

camera = PiCamera()

product_id="MyBox01"
flag=0

dbname= '/home/pi/Desktop/box/boxread.db'
#os.chdir('/home/pi/Desktop/box/video/')
#camera = picamera.PiCamera()
def getDHTdata():	
	DHT22Sensor = Adafruit_DHT.DHT22
	DHTpin = 22
	hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum
	
def logData (temp, hum,product_id,path,status):
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO dhtreadings values((?), (?),date('now'),time('now'), (?),(?),(?))", (temp, hum,product_id,path,status))
	conn.commit()
	conn.close()	


def record(name):
	camera.resolution = (1024, 768)
	camera.start_recording('/home/pi/Desktop/box/video/'+name+'.h264')
	sleep(15)
	camera.stop_recording()
	sleep(3)
	print(name)
	#name="2019-01-25_22-28-40"
	d=os.getcwd()
	os.chdir('/home/pi/Desktop/box/video/')
	convert = "MP4Box -add {}.h264 {}.mp4".format(name,name) #defining convert
	call ([convert], shell=True)
	os.system('rm '+name+'.h264')
	os.chdir(d)
	return 0

def _url(path):
    return 'http://18.233.171.56:8080/v1'+ path

def send_notification(ID):
     return requests.post(_url('/notifications/'), json=ID)
 
def verify_notification(id):
     return requests.get(_url('/notifications/{:s}/'.format(id)))
def update_passcodes(ID):
     return requests.post(url('/pass_codes/'), json=ID)

def create_passcodes(ID):
     return requests.put(_url('/pass_codes/'), json=ID)

def get_passcodes(id):
     #return requests.get(_url('/pass_codes/{:s}/'.format(id)))
	 return requests.get(_url(id))

ser = serial.Serial(
 port='/dev/ttyUSB0',
 baudrate = 9600,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)
counter=0
 
 
while 1:
		x=ser.readline()
		print x
 #data=json.dumps(x)

	#################### Password retrevig by arduino on startup ############


		time.sleep(1)
	#ser.write('Hi Aurdi')

	#if x=="query\r\n":
		# product_id="MyBox01"    
		#print("received")
		# f='/pass_codes/{:s}'.format(product_id)

		# resp=get_passcodes(f)

		

		# if resp.status_code != 200:

			# print(resp.status_code)
			# print('error shows not retrieved')


		# else:

			# print('done')
			# flag=1
			# result= resp.content.decode("utf-8")
			# j=json.loads(result)
			# ser.write(j['pass_code'].encode()) 
			# #ser.write(cert.encode(j['pass_code']))
		#flag=1	  
		#if flag==1:
	################## if password entered is correct ##########################
		#	while 1: 
		#		x=ser.readline()
		#		print x
		if x=="success\r\n":
			print('sending notification')  
			id=str(uuid.uuid4())
			ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] 
			#ID= {
			#			"notification_id" : id,
			#			"product_id" : "SmartBox-Test",
			#			"event" : "BOX_Opened",
			#			"event_ts" :ts
			#			}
						
			temp, hum = getDHTdata()
					
			status='Box Opened'
			name=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
			record(name)
			path=name+'.mp4'
			logData (temp, hum, product_id,path,status)	
			#resp=send_notification(ID)
			#if resp.status_code != 200:
			#	print(resp.status_code)
					#else:
			print('done')
				   
				################## if password entered is incorrect ##########################

		elif x=="unsuccessfull\r\n":
			print('sending notification')  
			id=str(uuid.uuid4())
			ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] 
		#	ID= {
		#			"notification_id" : id,
		#				"product_id" : "SmartBox-Test",
		#				"event" : "invalid password",
		#				"event_ts" :ts
		#				}
					
			status='Box Not Opened'
			temp, hum = getDHTdata()
			name=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
			record(name)
			path=name+'.mp4'
			logData (temp, hum, product_id,path,status)		
		#	resp=send_notification(ID)
		#		if resp.status_code != 200:
			#			print(resp.status_code)
			#		else:
			print('done')






