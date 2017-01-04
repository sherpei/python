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
threadstst.py
Threads usage in Python 2.7.2 in Telit HE910 module.
19/01/12 First version.
"""

import thread
import time

''''
import sys
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

print "\r\n\r\nThreads tests for HE910 Python 2.7.2 ver 20120120.1\r\n\r\n"

global lock, activethreads

def safe_print(msg):
    global lock
    lock.acquire()
    print msg
    lock.release()
    
def cronos( threadName, delay, cyclescount):
    count = 0
    global lock, activethreads
    while count < cyclescount:
        count += 1
        safe_print("%s run %d\r" % (threadName, count))
        # Delay with requested time
        time.sleep(delay)
        '''
        # Another way to do the delay
        start = time.time()
        while (time.time() - start < delay):
            pass
        '''
    activethreads = activethreads - 1

activethreads = 2
lock=thread.allocate_lock()
safe_print("Starting cronos #1 for 4 cycles of 2 seconds delay\r") 
thread.start_new_thread(cronos, ( "Cronos #1", 2.0, 4,))
safe_print("Starting cronos #1 for 6 cycles of 1 seconds delay\r")
thread.start_new_thread(cronos, ( "Cronos #2", 1.0, 6,))

while activethreads > 0:
    pass

print("\r\n\r\nBye bye!\r\n\r\n")


