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
testStrArg.py
Jan 2009|copyright added, checked & tested
02/05/07|Sgo|lt|1st ver
The script is to test the string allocation. It seems that no space is allocated
in the names list for the strings delimited by '' AND ending with \r.
removeCRfrom(string) is a function to use the string without \r
"""
#import MDM

#the following variables are not used in the code but loaded in the name space only if not terminated with \r
a='ATE1\r'
b="AT+GMR\r"
d='ATE1'

#the following variables are used in the code but loaded in the name space only if not terminated with \r
e='good'
f='good2\r'
g="best"
h="best2\r"

def removeCRfrom(string):
    a=string.endswith('\r')
    if a==1:
        b=string.split('\r')
        return b[0] 
    else:
        print "the string doesn't finish with \r "
        return ''

print 'testStrArg.py\r\n© 2009 Telit Communications\r'

a=removeCRfrom('ciao2\r')
print a
a=removeCRfrom('ciao')
print a
a=removeCRfrom("boh2\r")
print a
a=removeCRfrom("boh")
print a

a=removeCRfrom(e)
print a
a=removeCRfrom(f)
print a
a=removeCRfrom(g)
print a
a=removeCRfrom(h)
print a