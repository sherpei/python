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
ab_test.py
Jan 2009|copyright added, checked & tested
30/05/2008|Sgo|lt|1st ver
The script tries to open the test.bin file. If the file already exists, the program appends
some data, otherwise a new file is created with wb parameter.
"""

import sys

def tb_lineno(tb):
  # Coded by xxxxxxx from the example of PyCode_Addr2Line()
  # in compile.c.
  # Revised version by yyyyyyy to work with JPython too.
  c = tb.tb_frame.f_code
  if not hasattr(tb.tb_frame.f_code, 'co_lnotab'):
    return tb.tb_lineno

  line = tb.tb_frame.f_code.co_firstlineno
  addr = 0
  for i in range(0, len(tb.tb_frame.f_code.co_lnotab), 2):
    addr = addr + ord(tb.tb_frame.f_code.co_lnotab[i])
    if addr > tb.tb_lasti:
      break
    line = line + ord(tb.tb_frame.f_code.co_lnotab[i+1])
  return line

def read1000bytes(fileObj):
    Counter = 0
    fileObj.seek(0)    # from the beginning
    while(1):
            try:
                WS = fileObj.read(1000)
            except:
                WS = ''

            if len(WS) == 0:
                break                                               
            return WS
            
def opencreate(filename): 
    try:   
        print 'trying to open '+filename
        a=open(filename,"ab+")
        print 'open'+filename+'in ab+ mode'
        a.write('append this sentence')
        
        content=read1000bytes(a)     
        print 'Content',content
        
        a.flush()
        a.close()

        hndl=open(filename,"a+b")
        print 'open'+filename+'in a+b mode'
        hndl.write('append another sentence')

        content=read1000bytes(hndl)     
        print 'Content',content
        
        hndl.flush()
        hndl.close()        

        return 1
    except :
        import sys
        type, value, tb = sys.exc_info()
        # we get the exception caracteristics
        print'============= An Exception occurs ============'
        print 'Exception :', type, '=', value
        while tb is not None :
            print '  File "%s", line %d, in %s' % \
              (tb.tb_frame.f_code.co_filename,
               tb_lineno(tb),tb.tb_frame.f_code.co_name)
            tb = tb.tb_next
          # we transform the traceback exception in a string format.

        print " Trying to create new binary(b) file in w mode"
        hndl=open(filename,"wb")

        print "1 writing"
        hndl.write('writing type w -1')
        hndl.flush()

        #content=read1000bytes(hndl)    it doesn't read as for w mode (no w+) 
        print 'Content',content

        hndl.close()          
       
        return 0 

print 'ab_test.py\r\n© 2009 Telit Communications\r'
opencreate('test'+'.bin')
