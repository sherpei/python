# -*- coding: iso-8859-1 -*-
#Telit Extensions
#
#Copyright © 2009, Telit Communications S.p.A.
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
#Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in
#the documentation and/or other materials provided with the distribution.
#
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS``AS IS'' AND ANY EXPRESS OR IMPLIED
#WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY
#DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#POSSIBILITY OF SUCH DAMAGE.
#

"""
SKT_CL_SR.py
Feb 2012|corrected and tested for Python 2.7.2 on HE910
- added coding line on top
- changed MOD with time
- changed MDM.receive with MDM.read (see MDM_receive function)
- changed SER.receive with SER.read (see SER_receive function)
Jan 2009|copyright added, checked & tested
20/02/08|Sgo|ag|1st ver
the script allows to select a client/server device.
The script is composed by the following parts:

1) Script configuration (IP address, remote & local ports, APN, PIN, PUK, NET_Operator). 
2) Check SIM status, insert SIM PIN or PUK when needed, check for network registration
3) Socket configuration and GPRS context activation
4) Client or Server selection (external user/application and to send 'c' or 's' character to select one of the 2 options)
5a) Start Client mode dialing the remote socket (skt1)
5b) Start Server mode configuring firewall and socket listen (skt2) 
6) GPRS connection; every characted sent on the serial port of one module are received on the remote other port in trasparent way.
7) Suspend the socket with "+++" escape sequence.
8) Since MDM-SER bridge is active it is possible to send AT commands (AT#SO=skt to reconnect the socket; AT#SH=skt to close the connection)
9) The script is rebooted once DCD low status is detected.
"""

import time
import SER
import MDM

# ########################################################### #
# this values must be configured with valid ones..
# the ones here are only for demo.
# this is the network name to register to in manual mode
NETWORK     = "I TIM"  #  "I WIND"   "I TIM"   "vodafone IT"
PIN         = "1238"
PUK         = "53562047"
NEW_PIN     = "1238"
LOCAL_PORT  = "10500"
REMOTE_IP   = "217.202.102.128"
SUBNET_MASK = "255.0.0.0"
REMOTE_PORT = "10500"
APN         = "ibox.tim.it"
# 
# ########################################################### #

# ################# timeout definitions #######################
TIMEOUT_REG = 30
TIMEOUT_PIN = 100
TIMEOUT_MIN = 1
TIMEOUT_CMD = TIMEOUT_MIN * 10

def MDM_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
    return res

def SER_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + SER.read()
    return res

print 'SKT_CL_SR.py\r\n© 2009 Telit Communications\r'

time.sleep(4)
a = SER.set_speed('115200','8N1')


MDM.send('AT+CPIN?\r', 0)
res = MDM_receive(TIMEOUT_MIN)
SER.send('>res:' + res + '\n\r') # debug info

timer = time.time() + TIMEOUT_CMD
while ((res.find('SIM PIN')==-1) and (res.find('SIM PUK')==-1)and (res.find('READY')==-1) and (time.time() < timer) ):
	res = MDM_receive(TIMEOUT_MIN)
	# is it waiting pin?
if (res.find('SIM PIN')!=-1):
	# enter pin	
	# only for simulated environment
	#	pin = raw_input('Insert pin ')
	pin = PIN
	d = MDM.send('AT+CPIN=', 0)
	d = MDM.send(pin,0)
	d = MDM.send('\r',0)
	res = MDM_receive(TIMEOUT_MIN)

# is waiting puk?
elif (res.find('SIM PUK')!=-1):
# enter puk and new pin
# only for simulated environment
#	puk = raw_input('Insert puk ')
#	new_pin = raw_input('Insert new pin ')
	puk = PUK
	new_pin = NEW_PIN
	d = MDM.send('AT+CPIN=', 0)
	d = MDM.send(puk,0)
	d = MDM.send(',', 0)
	d = MDM.send(new_pin,0)
	d = MDM.send('\r',0)
	res = MDM_receive(TIMEOUT_MIN)

elif (res.find('READY')!=-1):
	res = MDM.send('AT+CPIN?\r', 0)
	res = MDM_receive(TIMEOUT_MIN)
	timeout = time.time() + TIMEOUT_PIN

# while SIM isn't ready and waiting time not timed out
while ((res.find('READY') == -1) and (time.time() < timer) ):
    res = MDM.send('AT+CPIN?\r', 0)
    res = MDM_receive(TIMEOUT_MIN)

if ( res != -1 ):
	print 'Pin OK\r'  

#get network registration status
res = MDM.send('AT+COPS?\r',0)
res = MDM_receive(5)
if( res.find(',') == -1):
    print 'No network\r'
else:
    print res

# only for simulated environment
# answer = raw_input('Do you want to register? Answer Y or N -> ')
# if (answer == "Y"):
# network = raw_input('network->')
if 1:
	network = NETWORK
	res = MDM.send('AT+COPS=1,0,"',0)
	res = MDM.send(network,0)
	res = MDM.send('"\r',0)
	res = MDM_receive(TIMEOUT_REG)
	res = MDM.send('AT+COPS?\r',0)
	res = MDM_receive(5)
	if( res.find(',') == -1):
	    print 'No network\r'
	else:
	    print res
time.sleep(5)
# Here start the GPRS session
s=''
while (s.find('OK')==-1) :				# configure the socket1
	MDM.send('AT#SCFG=1,1,512,0,200,10\r',0)
	s = MDM_receive(5)
	SER.send(s)  # debug info
	time.sleep(1)


while (s.find('OK')==-1) :				# configure the socket2
	MDM.send('AT#SCFG=2,1,512,0,200,10\r',0)
	s = MDM_receive(5)
	SER.send(s)  #debug info
	time.sleep(1)

s=''
while (s.find('OK')==-1) :
	a = SER.send('\rDEBUG_INFO : FIREWALL OFF\r')# debug info
	a = MDM.send('AT#FRWL=2\r',10)
	s = MDM_receive(5)
	a = SER.send(s)  # debug info      				
	time.sleep(1)

s=''
while (s.find('OK')==-1) :	
	a = MDM.send('AT+CGDCONT=1,"IP","',0)
	a = MDM.send(APN,0)			# insert APN of the operator in use (e.g.TIM)  'IBOX.TIM.IT' 
	a = MDM.send('"\r',0)
	s = MDM_receive(2)	
	time.sleep(1)

time.sleep(5)	
s=''
while (s.find('#SGACT')==-1) :
	a = SER.send('\rDEBUG_INFO : GPRS context\r')# debug info
	a = MDM.send('AT#SGACT=1,1\r', 10)     # GPRS context activation
	s = MDM_receive(5)
	a = SER.send(s)		# debug info
	time.sleep(1)



SER.send('Type "c" for CLIENT OR "s" for SERVER device:\r\n')
mode=''

while ((mode.find('c')==-1) and (mode.find('s')==-1)):
	mode = SER_receive(5)
	SER.send(mode)

	
print 'mode selected\c'
if (mode.find('c')!=-1):			 #if 'c' is received start client mode
	s=''
	print 'client\r'
	while (s.find('CONNECT')==-1) :    # OPEN the socket of the client
		a = SER.send('\rDEBUG_INFO : SKT DIAL\r')# debug info
		a = MDM.send('AT#SD=1,0,' + REMOTE_PORT + ',"' + REMOTE_IP + '",0,0\r', 10)  
		s = MDM_receive(20)
		a = SER.send(s)		# debug info
		time.sleep(1)
elif (mode.find('s')!=-1):			# if 's' is received start server mode
	s=''
	print 'server\r'
	while (s.find('OK')==-1) :      # set firewall
		a = SER.send('\rDEBUG_INFO : FIREWALL ON\r')# debug info
		a = MDM.send('AT#FRWL=1,"' + REMOTE_IP + '","' + SUBNET_MASK + '"\r', 10)
		s = MDM_receive(5)
		a = SER.send(s) 	# debug info
		time.sleep(1)


	s=''
	while (s.find('OK')==-1) :     # activate the socket listen
		a = SER.send('\rDEBUG_INFO : SKT LISTEN\r')# debug info
		a = MDM.send('AT#SL=2,1,' + LOCAL_PORT + ',0\r', 10)
		s = MDM_receive(5)
		a = SER.send(s) 	# debug info
		time.sleep(1)


	s=''
	while (s.find('CONNECT')==-1) : 	# wait for incoming connection indicated
		s = MDM_receive(10)		    # by SRING to answer and open the socket
		if (s.find('SRING: 2')!=-1) :
		  a = SER.send('\rDEBUG_INFO : SKT ANSW\r')# debug info
		  a = MDM.send('AT#SA=2\r', 10)
		  s = MDM_receive(5)
		  a = SER.send(s) 	# debug info
		else:  
		  time.sleep(1)

else:
	SER.send('Selection aborted\r')

if MDM.getDCD() == 1:
# a = SER.send('\rDEBUG_INFO : CONNECTED\r')
# res = SER.send('SOCKET OPEN') #debug info
    time.sleep(1)
# res = SER.send('START SENDING DATA')#debug info
 
# MDM.send(test,100)
n = 0
b = ""
m = 1

while MDM.getDCD() == 1:
    b = SER.read()
    s=""
    res = MDM.send(b, 10)
    s = MDM.read()
    # m = m + 1                  # in case you want to exit after m cycles
    rs = SER.send(s)
    # print "rs=" + str(rs) + " "
    # if m > 400:				# start the m cycle
       # MDM.send('+++', 10)
    # time.sleep(2) # 50
SER.set_speed('115200','8N1')    # this instruction reinitialize SER if got garbled
# res = SER.send('SOCKET CLOSED')#debug info

# print "\n\r" + "res=" + str(res) + "\n\r"

MDM.send('AT#REBOOT\r', 10)
