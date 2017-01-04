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
PowerSaving.py
Jan 2009|copyright added, checked & tested
14/10/06|Sgo|lt|1st ver
The script does a loop with the following operations:
puts the module in power saving for 5 minutes, then wakes up it , sends a string
to a server and it sleeps for 5 seconds
"""
import MDM
import MOD

##########################################
# User defined settings
# Edit according with your local values
##########################################
GPRS_APN = 'internet'           # GPRS APN, ask your network provider for correct values
GPRS_USER = ''                  # GPRS username
GPRS_PASSW = ''                 # GPRS password
SERVER_ADDR = 'byteworks.xxxx.xx'
SERVER_PORT = 10510
stringtosend = 'testing 123\r'  # string to be sent tthe server
##########################################
# End of User defined settings
##########################################

# other setings
TIMEOUT_CONNECT = 200           #20 seconds
TIMEOUT_MINIMUM = 10            # 1 second

print 'PowerSaving.py\r\n© 2009 Telit Communications\r'

print 'wait for the registration (about 25 seconds)\r'
MOD.sleep(250)

print 'configure PDP context with APN %s, username %s, password %s' % (GPRS_APN,GPRS_USER,GPRS_PASSW)
res = MDM.send('AT+CGDCONT=1,"IP","' + GPRS_APN + '"\r', 2)
res = MDM.receive(20)
res = res.find ('OK')
if (res == -1):
	print 'error setting PDP context\r'
	
if (GPRS_USER != ''):
    print 'set GPRS username\r'
    res = MDM.send('AT#USERID="'+ GPRS_USER + '"\r', 2)
    res = MDM.receive(20)
    res = res.find ('OK')
    if (res == -1):
        print 'error setting GPRS username\r'    

if (GPRS_PASSW != ''):
    print 'set GPRS password\r'
    res = MDM.send('AT#PASSW="'+ GPRS_PASSW + '"\r', 2)
    res = MDM.receive(20)
    res = res.find ('OK')
    if (res == -1):
        print 'error setting GPRS password\r' 

print 'activate GPRS context\r'
res = MDM.send('AT#GPRS=1\r',2)
res = MDM.receive(40)
print res
print 'after AT#GPRS=1\r'

print 'all settings done\r'

print "set CFUN=5, mobile full functionality with power saving enabled\r"
MDM.send("AT+CFUN=5\r", 5)
a = MDM.receive(10)
print a

trial = 0
print 'enter loop\r'
while (1 == 1):
    trial = trial + 1
    print '\r\n%d loop\r\n' % trial
    print "Set DTR 0 for 5 minutes:\r\n  enable Power Saving\r"
    
    MDM.setDTR(0)
    MOD.sleep(3000)

    print "Set DTR 1 : \r\n disable Power Saving"
    MDM.setDTR(1)

    print 'testing network registration\r'
    MDM.send("AT+CREG?\r", 5)
    a = MDM.receive(10)
    print a
    
    print 'connecting to %s port %d\r' % (SERVER_ADDR, SERVER_PORT)
    #initialize a connect timeout
    timer = MOD.secCounter()
    timeout = MOD.secCounter() + TIMEOUT_CONNECT
    res = MDM.send('AT#SKTD = 0,' + str(SERVER_PORT) + ',"' + SERVER_ADDR + '",255\r', 2)
    res = MDM.receive(TIMEOUT_MINIMUM)
    res = res.find('CONNECT')
    while ((res == -1)and (timer > 0) ):
        res = MDM.receive(TIMEOUT_MINIMUM)
        res = res.find('CONNECT')
        timer = timeout - MOD.secCounter()
    if ( res != -1 ):
        print 'CONNECTED\r'
    else:
        print 'fail to open socket!\r'

    print 'sending data to server: %s\r' % stringtosend
    res = MDM.send(stringtosend, 10)
    print 'waiting data from server\r'
    res = MDM.receive(100)	
    print res 

    print 'close socket\r'
    MOD.sleep(15)
    res = MDM.send('+++',10)
    MOD.sleep(15)
    
    print 'sleep 5 secondi before enetring in Power Saving again\r'
    MOD.sleep(50)

