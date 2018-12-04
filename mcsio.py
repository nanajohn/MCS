#!/usr/bin/python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
deviceId="D67fJsC9"
deviceKey ="qy2p0f1zjQh7w0sG"
import time
import sys
import Adafruit_DHT
import httplib,urllib
import json
deviceId="D67fJsC9"
deviceKey ="qy2p0f1zjQh7w0sG"
def post_to_mcs(payload): 
	headers = {"Content-type": "application/json", "deviceKey": deviceKey} 
	not_connected = 1 
	while (not_connected):
		try:
			conn = httplib.HTTPConnection("api.mediatek.com:80")
			conn.connect() 
			not_connected = 0 
		except (httplib.HTTPException, socket.error) as ex: 
			print("Error: %s"%ex)
			time.sleep(10)  
			# sleep 10 seconds 
	conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers) 
	response = conn.getresponse() 
	print( response.status, response.reason, json.dumps(payload), time.strftime("%c")) 
	data = response.read() 
	conn.close() 


while True:
	SwitchStatus = GPIO.input(14)
	if(SwitchStatus == 0):
		print('Button pressed')
	else:
		print('Button released')
	payload={"datapoints":[{"dataChnId":"SwitchStatus","values":{"value":SwitchStatus}}]} 
	post_to_mcs(payload)
	time.sleep(10) 
