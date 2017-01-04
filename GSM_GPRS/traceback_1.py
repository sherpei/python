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
traceback_1.py
Jan 2009|copyright added, checked & tested
14/12/06|Sgo|lt|1st ver
Gets exception details and formats them. 
"""

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

def main():
    print 'traceback_1.py\r\n© 2009 Telit Communications\r'
    r = 1 + ' ' # we generate an exception here

try:
  main()
except:
  # we catch it
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

