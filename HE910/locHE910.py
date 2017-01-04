import MDM
import SER
import time


GPRS_APN = ''                   # GPRS APN 
GPRS_USER = ''                  # GPRS username
GPRS_PASSW = ''                 # GPRS password

mcc = ''
mnc = ''
lac = ''
cellid = ''
datarec = ''


# waiting function
def Wait(sec):
    timer = time.time()
    timerstop = timer + sec
    while timer < timerstop:
        timer = time.time()



def MDM_receive(timeout):
    res = ''
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
    return res


def MDM_receiveUntil(value,timeout):
    res = ''
    found = -1
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
        found = res.find(value)
        if(found != -1):
            return res
            
    return res

def MDM_waitfor(value, timeout):
    res = ''
    found = -1
    start = time.time()
    while (time.time() - start < timeout):
        res = res + MDM.read()
        found = res.find(value)
        if(found != -1):
            return found
        
    return found


def GetData():
    Wait(2)
    data = ''
    timer = time.time()
    timeout = time.time() + 80 #seconds

    print 'start while'
    while(( MDM.getDCD() != 0) and (timer < timeout) ):
        data = data + MDM.read()
        
        timer = time.time()
        if(timer > timeout):
            print 'timeout reached'

        if(data.find('NO CARRIER') != -1):
            print 'no carrier reached'
            break

        if(MDM.getDCD() == 0):
            print 'DCD low'

    print 'out of while'
    print data
    
    if(len(data) == 0):
        print "ERROR: data to save is empty \r"
        return -1
        
    Wait(5)
    if MDM.getDCD() == 1:
        print 'connected'
        Wait(10)
        print 'disconnect'
        MDM.send('+++',10)
        Wait(10)
        myret = MDM_receive(50)
        print myret
    else:
        print 'DCD not active'

    return data


def ConnectIP( mcc, mnc, cellId, lac):
    global datarec
    
    print 'AT+WS46=25'
    MDM.send('AT+WS46=25\r',0)
    trovato = MDM_waitfor('OK', 10)
                
    if(trovato != -1):
        print 'ok go on '
    else:
        print  'error'
        return -1

    Wait(5)
    print 'configure PDP context with APN' +GPRS_APN+ ', username' + GPRS_USER
    Wait(4)
    print 'AT+CGDCONT=1,"IP","' + GPRS_APN + '"'
    res = MDM.send('AT+CGDCONT=1,"IP","' + GPRS_APN + '"\r', 2)
    res = MDM_waitfor('OK',20)
    if (res == -1):
        print 'error setting PDP context\r'
        return res

    print 'WAIT FOR GPRS ACTIVATION'
    Wait(5)

    print 'activate GPRS context\r'
    res = MDM.send('AT#SGACT=1,1\r',2)
    res = MDM_waitfor('OK',40)
    if (res == -1):
        print 'error activating GPRS'
        return res
	
    print 'all settings done\r'
    Wait(2)
    print 'connect to opencellid.org'
    res = MDM.send('AT#SD=1,0,80,"opencellid.org"\r', 2)
    res = MDM_waitfor('CONNECT',30)
    if (res == -1):
        print 'error connecting openall'
        return res

    strforserial = 'mmc = '+mcc+', mnc = '+mnc+', cellid = '+str(cellId)+', lac = '+str(lac)+'\r\n\r\n'
    SER.send(strforserial)
    strtocreate = 'GET http://www.opencellid.org/cell/get?mcc='+mcc+'&mnc='+mnc+'&cellid='+str(cellId)+'&lac='+str(lac)+'\r\n\r\n'
    print 'this is str to create'
    print strtocreate

    #datatosend = 'GET http://www.opencellid.org/cell/get?mcc=222&mnc=01&cellid=21093&lac=54717\r\n\r\n'
    
    res = MDM.send(strtocreate, 0)
    print 'GETTING DATA'
    #datarec = ''
    datarec = GetData()

    if(datarec != ''):
        print 'DOWNLOAD COMPLETE --- '
        print datarec
    else:
        print 'error data received void'

    print 'AT#SGACT=1,0'
    res = MDM.send('AT#SGACT=1,0\r',2)
    res = MDM_waitfor('OK',20)
    if (res == -1):
        print 'error deactivating GPRS'
        return res
    
    return 1
        
    


def GetCellValue( ):
    global mcc
    global mnc
    global lac
    global cellid

    SER.set_speed('115200')
    SER.send('start\r\n\r\n')


    print 'AT+WS46=12'
    MDM.send('AT+WS46=12\r',0)
    trovato = MDM_waitfor('OK', 10)
                
    if(trovato != -1):
        print 'ok go on '
    else:
        print  'error'
        return -1

    Wait(2)
    
    print 'AT+COPS=3,2'
    MDM.send('AT+COPS=3,2\r',0)
    trovato = MDM_waitfor('OK', 10)
    if(trovato != -1):
        print 'ok go on'
    else:
        print  'error AT+COPS=3,2'
        return -1

    MDM.send('AT+COPS?\r',0)
    mystr = MDM_receiveUntil('OK', 10)
    if(mystr != ''):
        print 'ok go on'
    else:
        print  'error AT+COPS?'
        return -1

    posit = mystr.find(',"')
    print posit
    if(posit != -1):
        print 'ok go on posit'
    else:
        print  'error'
        return -1

    print mystr[posit+2:]
    
    foundnbr = mystr[posit+2:].find('"')
    print foundnbr
    if(foundnbr != -1):
        print 'ok go on nbr found'
    else:
        print  'error'
        return -1

    tempstring1 =  mystr[posit+2:posit+2+foundnbr]
    print tempstring1
    mcc = tempstring1[:3]
    print mcc
    mnc = tempstring1[3:]
    print mnc

    
    
    
    print 'AT#MONI=0'
    MDM.send('AT#MONI=0\r',0)
    trovato = MDM_waitfor('OK', 10)
                
    if(trovato != -1):
        print 'ok go on'
    else:
        print  'error'
        return -1
                        
    print 'AT#MONI'
    MDM.send('AT#MONI\r',0)
    strmoni = MDM_receiveUntil('OK',12)
    print strmoni

    posit = strmoni.find('LAC:')
    print posit
    if(posit != -1):
        print 'ok go on posit'
    else:
        print  'error no LAC'
        return -1

    print strmoni[posit+4:]

    foundnbr = strmoni[posit+4:].find('Id:')
    print foundnbr
    if(foundnbr != -1):
        print 'ok go on Id found'
    else:
        print  'error'
        return -1

    print strmoni[posit+4:posit+4+foundnbr]

    #lac = strmoni[posit+4:posit+4+foundnbr].strip()
    lachex = strmoni[posit+4:posit+4+foundnbr].strip()
    print lachex
    lac = int(lachex,16)
    print lac

    foundId = strmoni[posit+4+foundnbr:].find('ARFCN:')
    if(foundnbr != -1):
        print 'ok go on ARFCN found'
    else:
        print  'error'
        return -1

    print strmoni[posit+7+foundnbr:posit+4+foundnbr+foundId]

    #cellid = strmoni[posit+7+foundnbr:posit+4+foundnbr+foundId].strip()
    cellidhex = strmoni[posit+7+foundnbr:posit+4+foundnbr+foundId].strip()
    print cellidhex
    cellid = int(cellidhex,16)
    print cellid

    return 1

def GetPosition(strlat):
    flat = strlat.find('cell lat=')
    if(flat != -1):
        print 'ok go on lat found'
    else:
        print  'error on lat'

    flatini = strlat[flat:].find('"')
    print strlat[flat+8:]
    if(flatini != -1):
        print 'ok go on lat found'
    else:
        print  'error on lat'

    flatend = strlat[flat+flatini+1:].find('"')
    if(flatend != -1):
        print 'ok go on lat end found'
    else:
        print  'error on lat'

    xlat = strlat[flat+flatini+1:]
    print xlat
    print xlat[:flatend]
    lat = xlat[:flatend]

    flon = xlat.find('lon=')
    if(flon != -1):
        print 'ok go on lon found'
    else:
        print  'error on lon'

    print xlat[flon:]
    flonini = xlat[flon:].find('"')  
    if(flonini != -1):
        print 'ok go on lon ini found'
    else:
        print  'error on lon'

    print xlat[flon+flonini+1:]

    flonend = xlat[flon+flonini+1:].find('"')
    if(flonend != -1):
        print 'ok go on lon end found'
    else:
        print  'error on lon'

    xlon = xlat[flon+flonini+1:]
    print xlon
    print xlon[:flonend]
    lon = xlon[:flonend]

    SER.send('Latitude:\r\n\r\n')
    SER.send(lat)
    SER.send('\r\n\r\n')
    SER.send('Longitude:\r\n\r\n')
    SER.send(lon)
    SER.send('\r\n\r\n')
    
    
ret = GetCellValue( )
if(ret != -1):
    val = ConnectIP(mcc, mnc, cellid, lac)
    if(val != -1):
        GetPosition(datarec)
        
 
