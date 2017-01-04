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
listenSMS.py
Jan 2009|copyright added, checked & tested
29/08/06|Sgo|lt|1st ver
The script receives the unsolicited result code if a SMS is received 
and print it on the debug, then collects the content of the SMS arrived
and print it on the debug
"""

# import the built-in modules
import MDM
import MOD

print 'listenSMS.py\r\n� 2009 Telit Communications\r'

#Iinitialize
print 'initialize\r'
MOD.sleep(100)
res = MDM.send('AT+CMGF=1\r', 0)            #select the text mode
res = MDM.receive(5)
res = MDM.send('AT+CNMI=2,1\r', 0)          #buffer unsolicited code and SMS memory location routed to the TE
res = MDM.receive(5)

pos = 0                                     #"position" string of the new SMS arrived
firstdigit_pos = 0                          #first digit of the "position" number of the new SMS arrived
res = MDM.receive(20)
print 'enter monitoring loop\r'
while 1:
    res = MDM.receive(20)                   #2 seconds
    a = res.find('+CMTI: "SM",')
    if  (a != -1):                          #the string '+CMTI: "SM",' is found
        firstdigit_pos = a+12
        pos = res[firstdigit_pos:-2]        #extract the position string of the new SMS arrived
        newSMSread_command = 'AT+CMGR='+str(pos)+'\r'
        print newSMSread_command            #for debug purposes
        MDM.send(newSMSread_command,5)      #read the new SMS arrived
        SMScontent = MDM.receive(15)        #collect the content
        print SMScontent                    #for debug purposes
    #else:
    #    print a + '\r'                      #for debug purposes
    #print pos + '\r'                        #for debug purposes
    
    
    
   

