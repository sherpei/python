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
FTP.py
Feb 2012|corrected and tested for Python 2.7.2 on HE910
- added coding line on top
- changed MOD with time
- changed MDM.receive with MDM.read (see MDM_receive function)
Jan 2009|copyright added, checked & tested
06/11/06|Sgonico|fb&lt|1st ver
Demonstrates FTP operations.
"""
import time
import SER
import MDM

##########################################
# User defined settings
# Edit according with your local values
##########################################
SIMPIN = '***'
GPRS_APN = 'internet'           # GPRS APN, ask your network provider for correct values
GPRS_USER = ''                  # GPRS username
GPRS_PASSW = ''                 # GPRS password
FTPSERVER_ADDR = 'ftp.byte****.***'
FTPUSERNAME = '*****'
FTPPASSWORD = '*****'
FTPFILECONTENT = 'testing 123'
##########################################
# End of User defined settings
##########################################

def MDM_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
    return res


print 'FTP.py\r\n� 2009 Telit Communications\r'

print 'SIM PIN  %s\r\n' % (SIMPIN)
res = MDM.send('AT+CPIN=' + SIMPIN + '"\r', 2)
res = MDM_receive(2)
print res
res = res.find ('OK')
if (res == -1):
	print 'error setting SIM PIN\r'

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

print 'all settings done\r'

s=''
print 'open ftp\r'
while (s.find('OK')==-1) :
	a = MDM.send('AT#FTPOPEN="' + FTPSERVER_ADDR + '","' + FTPUSERNAME + '","' + FTPPASSWORD + '",0\r', 5)
	s = MDM_receive(5)
	print s,'\r'
	time.sleep(1)

print 'set ftp file transfer mode to text\r'
s = ''
while (s.find('OK')==-1) :
	a = MDM.send('AT#FTPTYPE=1\r', 5)
	s = MDM_receive(5)
	print s,'\r' 
	time.sleep(1)

print 'initiate ftp put\r'
s = ''
while (s.find('CONNECT')==-1) :
	a = MDM.send('AT#FTPPUT="file1.txt"\r', 5)
	s = MDM_receive(5)
	print s,'\r' 
	time.sleep(1)

if MDM.getDCD() == 1:
    print 'connected\r'
    time.sleep(1)
    a = MDM.send(FTPFILECONTENT, 5)
    s = MDM_receive(5)
    print s,'\r'
    print 'disconnecting\r'
    time.sleep(2)
    MDM.send('+++',10)
    time.sleep(2)
    s = MDM_receive(5)
    print s,'\r'
    time.sleep(1)

print 'sleeping 5 seconds\r'    
time.sleep(5)
print 'initiate file get\r' 
s = ''
while (s.find('CONNECT')==-1) :
	a = MDM.send('AT#FTPGET="file1.txt"\r', 10)
	s = MDM_receive(1)
	print s,'\r'
	time.sleep(2)
	s = MDM_receive(2)
	print s,'\r'

print 'Done\r'

