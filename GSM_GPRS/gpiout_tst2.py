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
gpiout_tst2.py
Jan 2009|copyright added, checked & tested
04/01/07|Sgo|lt|1st ver
the script sets the GPIO5 as a GPIO output and cycles between 1 and 0 value
with a clock period of aprox. 2.4 seconds
"""

import MOD
import GPIO

print 'gpiout_tst2.py\r\n© 2009 Telit Communications\r'


GPIO_I  = 2         # GPIO used for SCL pin
GPIO_II  = 4        # GPIO used for SDA pin


GPIO.setIOdir(GPIO_I,0,1)
GPIO.setIOdir(GPIO_II,0,1)

i=1
while 1:
    print 'loop %d\r' % i
    print 'cycle GPIO_1\r'
    GPIO.setIOvalue(GPIO_I,1)
    MOD.sleep(2)    #0.2 secs
    GPIO.setIOvalue(GPIO_I,0)
    MOD.sleep(2)
    
    print 'cycle GPIO_2\r'
    GPIO.setIOvalue(GPIO_II,1)
    MOD.sleep(2)    #0.2 secs
    GPIO.setIOvalue(GPIO_II,0)
    
    print 'sleep 2 seconds\r'
    MOD.sleep(20)
    
    i = i + 1
