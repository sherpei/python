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
fdi.py
Feb 2012|corrected and tested for Python 2.7.2 on HE910
- added coding line on top
- modified file path to /sys folder
- changed MOD to time
- changed MDM.receive with MDM.read (see MDM_receive function)
Jan 2009|copyright added, checked & tested
14/12/06|Sgo|lt|1st ver
Unexpected power loss with file left open.
"""

import time
import MDM

def MDM_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
    return res

def Main():
    print 'start', time.time()
    en2_str = '9876543210\r\n'
    
    f=open('/sys/test.txt','w')
    for i in range(2000):
        f.write(en2_str)
    f.flush()
    # test what happens if power is lost before closing the file
    # consider that the write and flush operation last 100ms and hence can be roughly considered "atomic"
    # while open and close last much more..
    #f.close()   
    print 'end-2', time.time()
    MDM.send('AT#escript=""\r',10)
    # now disable the script so that next boot will not change the file written...
    print 'disable script', MDM_receive(1)

print 'fdi.py\r\n� 2009 Telit Communications\r'
Main()
    