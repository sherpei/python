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
ADC_test.py
Feb 2012|corrected and tested for Python 2.7.2 on HE910
- added coding line on top
- changed MOD with time
- changed MDM.receive with MDM.read (see MDM_receive function)
Jan 2009|copyright added, checked & tested
16/10/06|Sgo|lt|1st ver
The script does a loop with the following operations:
measures the ADC value at the ADC_IN1 pin, by issuing AT#ADC and AT#ADC=1,2,
then using GPIO.getADC, then prints the result on the debug port, sleeps for 
0,5 sec
(the permitted Vmax of the input is 2V)
"""

import MDM
import time
import GPIO

def MDM_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
    return res

MDM.send("AT#ADC\r", 5)
a = MDM_receive(2)
print "AT#ADC:%s\r" % a
    
print 'sleep 1 second\r'
time.sleep(5)

trial = 0
while (1 == 1):
    trial = trial + 1
    print 'loop %d:\r' % trial
        
    MDM.send("AT#ADC=1,2\r", 5)
    a = MDM_receive(2)
    print "\tAT#ADC=1,2 --> %s\r" % a

    mv = GPIO.getADC(1)
    print "GPIO.getADC(1) --> %d mV\r" % mv
    
    print 'sleep 1 second\r'
    time.sleep(1)
        

