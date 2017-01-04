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
FSys_mngtst2.py
Feb 2012|corrected and tested for Python 2.7.2 on HE910
- added coding line on top
- modified file path to /sys folder
Jan 2009|copyright added, checked & tested
31/10/2007|Sgo|lt|1st ver
Modify a byte in a file test2.txt of 4000 Bytes stored in NVM, at  5th position
"""

import sys
            
def opencreate(filename): 
    curr_posit=0
    try:
        print 'trying to open %s\r' % filename
        f=open(filename,"r+")
        print 'open %s\r' % filename
        curr_posit=f.tell()     #test tell method   
        print 'current position %d\r' % curr_posit
        f.seek(curr_posit+5)
        f.write('d')
        f.flush()
        f.close()
        return 1
    except : 
        v=sys.exc_info() 
        print "Error opening file : %s\r" % str(v)         
        return 0 

print 'FSys_mngtst2.py\r\n© 2009 Telit Communications\r'
opencreate('/sys/test8'+'.txt')
