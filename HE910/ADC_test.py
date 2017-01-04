import MDM
import time
import GPIO

def MDM_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
    return res

MDM.send("AT#ADC\r", 5)
a = MDM_receive(2)
print "AT#ADC:%s\r" % a
    
print 'sleep 1 second\r'
time.sleep(5)

trial = 0
while (1 == 1):
    trial = trial + 1
    print 'loop %d:\r' % trial
        
    MDM.send("AT#ADC=1,2\r", 5)
    a = MDM_receive(2)
    print "\tAT#ADC=1,2 --> %s\r" % a

    mv = GPIO.getADC(1)
    print "GPIO.getADC(1) --> %d mV\r" % mv
    
    print 'sleep 1 second\r'
    time.sleep(1)
        

