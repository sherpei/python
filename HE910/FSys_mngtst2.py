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
