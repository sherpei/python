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
SER_MDM_bridge.py
Feb 2012|corrected and tested for Python 2.7.2 on HE910
- added coding line on top
- changed MOD with time
- changed MDM.receive with MDM.read (see MDM_receive function)
- changed SER.receive with SER.read (see SER_receive function)
Jan 2009|copyright added, checked & tested
Idea for a bi-directional SER to MDM bridge, useful in serial cable to wireless
applications. It shows only the core of the implementation, other things like
module setup and GPRS and serial connections initiation and finalization must
be build around. One must play with different settings, flow control, timings
etc. to shape on different application details.
"""

import MDM
import SER
import time

def MDM_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
    return res

def SER_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + SER.read()
    return res

print 'SER_MDM.py\r\n© 2009 Telit Communications\r'

in_ = ''
out = ''

while (out.find('NO CARRIER') == -1):
	out = MDM_receive(1)
	SER.send(out)
	# time.sleep(1) # 1 second way too much
	in_ = SER_receive(10)
	MDM.send(in_,10)
