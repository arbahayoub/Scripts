# Use the following command to generate Tor password :
# tor.exe --hash-password torControlPortPassword | more

# Add the following line in "%USERPROFILE%\Desktop\Tor Browser\Browser\TorBrowser\Data\Tor\torrc" file
# HashedControlPassword 16:F3EA6F339A789FF16024850EBCD07CFFA36B60DCB1316F7F0ADEB6D507

# Start tor using the following comand
# "%USERPROFILE%\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe" --ControlPort 9051

import requests
import socket
import time
import threading
import urllib3
import re

urlPublicIP = "https://api.ipify.org"
IPLogFile = "TorIPLog.txt"
proxyHost = "127.0.0.1"
proxyPort = "8888"
torHost = "127.0.0.1"
torControlPort = "9051"
torControlPortPassword = "torControlPortPassword"
changeIpAddressFrequency = 60
getIpAddressFrequency = 5

def changeIpAddress():
	serverSocket = socket.socket()
	serverSocket.connect((torHost, int(torControlPort)))
	serverSocket.send(('AUTHENTICATE "'+torControlPortPassword+'"\r\nSIGNAL NEWNYM\r\n').encode())

previousIPAddress = ''
def getIpAddress():
	global previousIPAddress
	torProxies = {
		'http':  proxyHost+':'+proxyPort,
		'https': proxyHost+':'+proxyPort
	}
	session = requests.session()
	session.proxies = torProxies
	currentIPAddress = session.get(urlPublicIP, verify=False).text
	if re.search("^[0-9]+.[0-9]+.[0-9]+.[0-9]+$", currentIPAddress) and previousIPAddress != currentIPAddress:
		currentTime = time.strftime("%H:%M:%S", time.localtime())
		file = open(IPLogFile, "a")
		file.write(currentTime+" "+currentIPAddress+"\n")
		file.close()
		print(currentTime+" "+currentIPAddress)
		previousIPAddress = currentIPAddress

def executeFrequently(function, delay):
	timer = threading.Timer(delay, executeFrequently, [function, delay])
	timer.daemon = True
	timer.start()
	function()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
if __name__ == "__main__":
	executeFrequently(changeIpAddress, changeIpAddressFrequency)
	executeFrequently(getIpAddress, getIpAddressFrequency)
	try:
		while True:
			time.sleep(1)
	except:
		pass