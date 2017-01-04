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
watchd_test.py
Jan 2009|copyright added, checked & tested
11/09/06|Sgo|lt|1stver
this script is a test for the watchdog function:
when the "i" loop counter reaches 2000, module enters sleep for 70 seconds starts:
after 60 secs of the 70 secs the module restarts due to watchdog
"""
import MDM
import MOD

print 'watchd_test.py\r\n© 2009 Telit Communications\r'

print 'enable watchdog with 60 seconds timeout\r'
a=MOD.watchdogEnable(60)
print a,'\r'
a=MOD.watchdogReset()

i=0
while 1:
    print 'loop %d\r' % i
    MOD.watchdogReset()         # to avoid the module restarts in the middle of the loop
                                # during it's carrying out useful operations    
    if i == 2000:
        print 'enter sleep\r'
        MOD.sleep(700)          # the script sleeps for 70 seconds:
                                #the watchdog counter doesn't reset before the Enable timeout is expired: the module will restart
    i = i+1                     #increase the loop counter

MOD.watchdogDisable()           #disable watchdog (useful if the module exits successfully from the while loop)
print 'this sentence will not be ever printed\r'

    
    

 