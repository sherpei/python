#Telit Extensions
#
#Copyright(c) 2012, Telit Communications S.p.A.
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
floattst.py
Hihglights of float type implementation in Python 2.7.2 in Telit HE910 module.
18/01/12 First version.
"""

import sys
import time

''''
import SER
#If debugging on SER is desired use this trick.
class SERstdout:
    def __init__(self):
        SER.set_speed("115200","8N1")
    def write(self,s):
        SER.send(s)

if(sys.platform != "win32"):
    sys.stdout = SERstdout()
    sys.stderr = SERstdout()
''' 

print "\r\n\r\nFloat type tests for HE910 Python 2.7.2 ver 20120118.1\r\n"

print "\r\n\r\n"

print "How to 'cast' numbers to float type\r\n"
print "Type of 3 is \n"
print type(3)
print "\r\n"

print "Type of 3.0 is \n"
print type(3.0)
print "\r\n"

print "Type of -3 is \n"
print type(-3)
print "\r\n"

print "Type of -3.0 is \n"
print type(-3.0)
print "\r\n"

print "How to force float arithmetic operations\r\n"
print "Result of 4/8 is ", 4/8 , " of type"
print type(4/8)
print "\r\n"

print "Result of 9/3 is ", 9/3 , " of type"
print type(9/3)
print "\r\n"

print "Result of 4.0/8 is ", 4.0/8 , " of type"
print type(4.0/8)
print "\r\n"

print "Result of 4/8.0 is ", 4/8.0 , " of type"
print type(4/8.0)
print "\r\n"

print "Result of 9.0/3 is ", 9.0/3 , " of type"
print type(9.0/3)
print "\r\n"

print "Result of 9/3.0 is ", 9/3.0 , " of type"
print type(9/3.0)
print "\r\n"

print "Result of 12.7/48.3 is ", 12.7/48.3 , " of type"
print type(12.7/48.3)
print "\r\n"

print "Square root\r\n"
print "Result of 4**0.5 is ", 4**0.5 , " of type"
print type(4**0.5)
print "\r\n"

print "Result of 3**0.5 is ", 3**0.5 , " of type"
print type(3**0.5)
print "\r\n"

print "String formating with floats\r\n"
print "12.7/48.3 prints: ", 12.7/48.3, "\r"
print "format(12.7/48.3, '.5f') prints: ", format(12.7/48.3, '.5f'), "\r"
print "format(12.7/48.3, '.2f') prints: ", format(12.7/48.3, '.2f'), "\r"
print "\r\n"

print "MOD module isn't available, use time module instead\r\n"
print "time.clock() is: ", time.clock(), " of type"
print type(time.clock())
print "\r\n"
print "time.time() is: ", time.time(), " of type"
print type(time.time())
print "\r\n"
print "Use time.sleep(secondsfloatval) instead of MOD.sleep()\r\n"
print "Sleeping now for 2.5 seconds with time.sleep(2.5)\r\n"
time.sleep(2.5)
print "\r\n\r\n"
print "Bye bye!\r\n\r\n"
