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
send_email.py
Jan 2009|copyright added, checked & tested
Sends email using #SEMAIL command
"""

import MDM 
import MOD 

##########################################
# User defined settings
# Edit according with your local values
##########################################
GPRS_APN = 'internet'                   # GPRS APN, ask your network provider for correct values
GPRS_USER = ''                          # GPRS username
GPRS_PASSW = ''                         # GPRS password
SMTP_SERVER   = "bytexxxx.xxx"          # SMTP server
SMTP_USERID   = "info@bytexxxx.xxx"     # SMTP username
SMTP_PASSW    = "xxxxxxxxxx"            # SMTP password
FROM_EMAIL_ADDR = "info@bytexxxx.xxx"   # SMTP FROM
TO_EMAIL_ADDR = "info@thexxxxxxxxxx.xx" # SMTP TO
SUBJECT = "test"                        # email subject
BODY = "testing 123"                    # email body
##########################################
# End of User defined settings
##########################################

print 'send_email.py\r\n© 2009 Telit Communications\r'

print "loop waiting modem network registration\r", 
while(1): 
    res = MDM.send('AT+CGREG?\r',2) 
    res = MDM.receive(20) 
    if (res.find ('+CGREG: 0,1') != -1): 
        print "[OK]\r" 
    break 
    MOD.sleep(50) 
    
while(1): 
    print "set GPRS parameters\r", 
    tmp = "AT+CGDCONT=1,\"IP\",\"%s\"\r" % GPRS_APN
    res = MDM.send(tmp,2) 
    res = MDM.receive(10) 
    if(res.find ('OK')==-1): 
        print "[ERROR +CGDCONT]\r" 
        break 
    tmp = "AT#USERID=\"%s\"\r" % GPRS_USER 
    res = MDM.send(tmp,2) 
    res = MDM.receive(10) 
    if(res.find ('OK')==-1): 
        print "[ERROR #USERID]\r" 
        break 
    tmp = "AT#PASSW=\"%s\"\r" % GPRS_PASSW
    res = MDM.send(tmp,2) 
    res = MDM.receive(10) 
    if(res.find ('OK')==-1): 
        print "[ERROR #PASSW]\r" 
        break 
    print "[OK]" 
    
    print "set SMTP parameters\r" 
    tmp = "AT#ESMTP=\"%s\"\r" % SMTP_SERVER 
    res = MDM.send(tmp,2) 
    res = MDM.receive(10) 
    print res 
    tmp = "AT#EUSER=\"%s\"\r" % SMTP_USERID 
    res = MDM.send(tmp,2) 
    res = MDM.receive(10) 
    print res 
    tmp = "AT#EPASSW=\"%s\"\r" % SMTP_PASSW 
    res = MDM.send(tmp,2) 
    res = MDM.receive(10) 
    print res 
    tmp = "AT#EADDR=\"%s\"\r" % FROM_EMAIL_ADDR 
    res = MDM.send(tmp,2) 
    res = MDM.receive(10) 
    print res
            
    print "GPRS context must be de-activated\r", 
    timer=MOD.secCounter() 
    while 1:
        res = MDM.send('AT#GPRS=0\r', 2) 
        res = MDM.receive(40)
        print 'Context deactivation:\r',res
    
        res = MDM.send('AT+CGATT?\r', 2) 
        res = MDM.receive(20) 
        if(res.find("+CGATT: 1")!=-1): 
            print "[OK]\r" 
            break       
        
    print "send email\r", 
        
        
    res = MDM.send('AT#SEMAIL="', 2) 
    res = MDM.send(TO_EMAIL_ADDR, 2) 
    res = MDM.send('",', 2) 
    res = MDM.send( SUBJECT + '\r', 2) 
    print 'should get > prompt:\r'
    res = MDM.receive(90) 
    print res 
    print 'send body\r'
    res = MDM.send(BODY, 2) 
    print res 
    print 'send termination character\r'
    res = MDM.send('\x1a', 2) 
    print res 
    print 'sleep some time before reading the result\r'
    MOD.sleep(200) 
    res = MDM.read() 
    if(res.find ('OK')==-1): 
         print "[ERROR EMAIL]\r" 
    else: 
         print "[OK]\r" 
         print "email sent succesfully\r" 

    print 'sleep 1 minute before sending again\r'
    MOD.sleep(600)

 



