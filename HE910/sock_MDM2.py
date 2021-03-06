# -*- coding: iso-8859-1 -*-
#Telit Extensions
#
#Copyright � 2009, Telit Communications S.p.A.
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
sock_MDM2.py
Feb 2012|corrected and tested for Python 2.7.2 on HE910
- added coding line on top
- changed MOD with time
- changed MDM.receive with MDM.read (see MDM_receive function)
- changed MDM2.receive with MDM2.read (see MDM2_receive function)
Jan 2009|copyright added, checked & tested
28/08/07|Sgo|lt|1st ver
Sends data to a server through a TCP socket on MDM while using MDM2 for other
actions
"""

import MDM
import time
import MDM2

##########################################
# User defined settings
# Edit according with your local values
##########################################
GPRS_APN = 'internet'           # GPRS APN, ask your network provider for correct values
GPRS_USER = ''                  # GPRS username
GPRS_PASSW = ''                 # GPRS password
SERVER_ADDR = 'byte*****.****.***'
SERVER_PORT = 10510
stringtosend = 'testing 123\r'  # string to be sent tthe server
##########################################
# End of User defined settings
##########################################

# other setings
TIMEOUT_CONNECT = 20           #20 seconds
TIMEOUT_MINIMUM = 1             # 1 second

def MDM_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
    return res

def MDM2_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM2.read()
    return res

print 'sock_MDM2.py\r\n� 2009 Telit Communications\r'

print 'wait for the registration (about 25 seconds)\r'
time.sleep(25)

print 'configure PDP context with APN %s, username %s, password %s' % (GPRS_APN,GPRS_USER,GPRS_PASSW)
res = MDM.send('AT+CGDCONT=1,"IP","' + GPRS_APN + '"\r', 2)
res = MDM_receive(2)
res = res.find ('OK')
if (res == -1):
	print 'error setting PDP context\r'
	
if (GPRS_USER != ''):
    print 'set GPRS username\r'
    res = MDM.send('AT#USERID="'+ GPRS_USER + '"\r', 2)
    res = MDM_receive(2)
    res = res.find ('OK')
    if (res == -1):
        print 'error setting GPRS username\r'    

if (GPRS_PASSW != ''):
    print 'set GPRS password\r'
    res = MDM.send('AT#PASSW="'+ GPRS_PASSW + '"\r', 2)
    res = MDM_receive(2)
    res = res.find ('OK')
    if (res == -1):
        print 'error setting GPRS password\r' 

print 'activate GPRS context\r'
res = MDM.send('AT#GPRS=1\r',2)
res = MDM_receive(4)
print res
print 'after AT#GPRS=1\r'

#initialize a connect timeout
timer = time.time()
timeout = time.time() + TIMEOUT_CONNECT

print 'all settings done\r'

cd = MDM.getDCD()
print "DCD before at#sktd, read on MDM: %d\r" % cd
cd = MDM2.getDCD()
print "DCD before at#sktd, read on MDM2: %d\r" % cd

print 'connecting to %s port %d\r' % (SERVER_ADDR, SERVER_PORT)
res = MDM.send('AT#SKTD = 0,' + str(SERVER_PORT) + ',"' + SERVER_ADDR + '",255\r', 2)
res = MDM_receive(TIMEOUT_MINIMUM)
res = res.find('CONNECT')
while ((res == -1)and (timer > 0) ):
    res = MDM_receive(TIMEOUT_MINIMUM)
    res = res.find('CONNECT')
    timer = timeout - time.time()
if ( res != -1 ):
    print 'CONNECTED\r'
else:
    print 'fail to open socket!\r'

cd = MDM.getDCD()
print "DCD after at#sktd, read on MDM: %d\r" % cd
cd = MDM2.getDCD()
print "DCD after at#sktd, read on MDM2: %d\r" % cd

print 'sending data to server: %s\r' % stringtosend
res = MDM.send(stringtosend, 10)
print 'waiting data from server\r'
res = MDM_receive(10)	
print res 

cd = MDM.getDCD()
print "DCD after data transfer, read on MDM: %d\r" % cd
cd = MDM2.getDCD()
print "DCD after data transfer, read on MDM2: %d\r" % cd

print 'query #MONI on MDM2\r'
MDM2.send('AT#MONI\r',0)
data = MDM2_receive(4)
print 'RESPONSE to AT#MONI: %s' % data

cd = MDM.getDCD()
print "DCD after #MONI, read on MDM: %d\r" % cd
cd = MDM2.getDCD()
print "DCD after #MONI, read on MDM2: %d\r" % cd

print 'close the socket\r'
time.sleep(2)
res = MDM.send('+++',10)
time.sleep(2)

time.sleep(5)
cd=MDM.getDCD()
cd = MDM.getDCD()
print "DCD 5 seconds after closing socket, read on MDM: %d\r" % cd
cd = MDM2.getDCD()
print "DCD 5 seconds after closing socket, read on MDM2: %d\r" % cd
