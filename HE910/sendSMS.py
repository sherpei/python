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
sendSMS_.py
Feb 2012|corrected and tested for Python 2.7.2 on HE910
- added coding line on top
- changed MOD with time
- changed MDM.receive with MDM.read (see MDM_receive function)
12/09/06|Sgo|lt|1st ver
Jan 2009|copyright added, checked & tested
The script sends a SMS to a destination number in text mode
"""
import MDM
import time

##########################################
# User defined settings
# Edit according with your local values
##########################################
SMSTO = '072*******'                        # recipient number for the SMS
SMSTEXT = 'testing 123'                     # SMS text
##########################################
# End of User defined settings
##########################################

def MDM_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
    return res

print 'sendSMS.py\r\n© 2009 Telit Communications\r'

print 'wait network registration\r'
while (1 == 1):
    a = MDM.send('AT+CREG?\r',2)
    res = MDM_receive(1)
    print res,a,'\r'
    if (res.find('0,1') != -1) or (res.find('1,1') != -1) or (res.find('0,2') != -1) or (res.find('1,5') != -1):
        print "registered\r"
        break
    else:
        time.sleep(1)

print 'set text mode\r'
a = MDM.send('AT+CMGF=1\r', 2)
res = MDM_receive(1)
print res,a,'\r'

print 'sleep 5 seconds\r'
time.sleep(5)

print 'send SMS\r'
a = MDM.send('AT+CMGS="' + SMSTO + '"\r', 2)
print 'waiting 1 second for > prompt\r'
res = MDM_receive(1)
print res,a,'\r'
a = MDM.send(SMSTEXT, 2)
print 'send termination character CTRL-Z\r'
a = MDM.sendbyte(0x1A, 2)
print a,'\r'

print 'done\r'


