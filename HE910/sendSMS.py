
"""
sendSMS_.py

The script sends a SMS to a destination number in text mode
"""
import MDM
import time

##########################################
# User defined settings
# Edit according with your local values
##########################################
SMSTO = '072*******'                        # recipient number for the SMS
SMSTEXT = 'testing 123'                     # SMS text
##########################################
# End of User defined settings
##########################################

def MDM_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
    return res

print 'sendSMS.py\r\n© 2009 Telit Communications\r'

print 'wait network registration\r'
while (1 == 1):
    a = MDM.send('AT+CREG?\r',2)
    res = MDM_receive(1)
    print res,a,'\r'
    if (res.find('0,1') != -1) or (res.find('1,1') != -1) or (res.find('0,2') != -1) or (res.find('1,5') != -1):
        print "registered\r"
        break
    else:
        time.sleep(1)

print 'set text mode\r'
a = MDM.send('AT+CMGF=1\r', 2)
res = MDM_receive(1)
print res,a,'\r'

print 'sleep 5 seconds\r'
time.sleep(5)

print 'send SMS\r'
a = MDM.send('AT+CMGS="' + SMSTO + '"\r', 2)
print 'waiting 1 second for > prompt\r'
res = MDM_receive(1)
print res,a,'\r'
a = MDM.send(SMSTEXT, 2)
print 'send termination character CTRL-Z\r'
a = MDM.sendbyte(0x1A, 2)
print a,'\r'

print 'done\r'


