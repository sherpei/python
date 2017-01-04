import time
import SER
import MDM
#import _md5


GPRS_APN = ''                   # GPRS APN 
GPRS_USER = ''                  # GPRS username
GPRS_PASSW = ''                 # GPRS password
FTPSERVER_ADDR = ''
FTPUSERNAME = ''
FTPPASSWORD = ''


TIMEOUT_ATTESA = 5
TIMEOUT_CMD = 5

DISC_LEN = 25	# len of end sequence with NO CARRIER
START_LEN = 7   # len of CONNECT
#MD5_LEN = 15	# len of md5 sequence


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

def delsms(SMSindex):
    
    indice = str (SMSindex)
    print 'index :'
    print indice
    print 'at+cmgd=' + indice
    MDM.send('at+cmgd=', 0)
    MDM.send(indice,0)
    MDM.send('\r',0)
    res = MDM_waitfor('OK',20)
    if(res == -1):
        print 'error deleting sms'
    print res

def sendsms(NUM,TEXT):
    res = MDM.send('AT+CMGS=', 0)
    res = MDM.send(NUM, 0)
    res = MDM.sendbyte(0x0d, 0)
    res = MDM_receiveUntil('>',10)
    if(res == -1):
        print 'error sending sms'
        MDM.sendbyte(0x1b,0)
        return -1
        
    res = MDM.send(TEXT, 0)
    res = MDM.send('\x1a', 0)
    print 'sending sms ...'
    return 1

def SmsSetup():
    a = MDM.send('AT+CMGF=1\r', 0)
    print 'AT+CMGF=1\r'
    trovato = MDM_waitfor('OK', 10)
    print trovato
    a = MDM.send('AT+CNMI=2,1\r', 0)
    print 'AT+CNMI=2,1\r'
    trovato = MDM_waitfor('OK', 10)
    print trovato

def findSmsPos(stri):
    foundPos = -1

    foundPos = stri.find('"SM"')
    print foundPos
    temp = ''
    if(foundPos != -1):
        temp = stri[foundPos+5:]
        print temp

    return temp


def LookforSMS(txt):
    foundPos = -1
    strtxt = ''
    strd2 = ''
    strd3 = ''

    foundPos = txt.find('+CMGR:')
    if(foundPos != -1):
        strtxt = txt[foundPos+5:]
        print strtxt
    else:
        print 'error pos'
        return strtxt

    findendl = strtxt.rfind('"')
    if(findendl != -1):
        strd2 = strtxt[findendl+1:]
        print strd2
    else:
        print 'error endl'
        return strd2


    findok = strd2.find('OK')

    if(findok != -1):
        strd3 = strd2[:findok-2]
        print strd3
    else:
        print 'error: Ok not found looking for SMS'
        return strd2
    
    return strd3

def ExtraxtNUM(SMStext,cmd):
     fend = -1
     comma = -1
     found = SMStext.find(cmd)
     lcmd = len(cmd)
     if(found == -1):
          print 'no find +CMGR'
          return -1
     else:
          print 'ok +CMGR found'
          fend = SMStext.rfind('"')
          if(fend == -1):
               print 'no end line'
               return -1

          comma = SMStext.find(',')
          if(comma == -1):
               print 'error comma not found'
               return -1

          data = SMStext[comma+2 : fend]
          print data
          numpos = data.find('"')
          if(numpos == -1):
               print 'error finding number'
               return -1

          number = data[:numpos]
          print number

          return number


def ExtraxtNAMEFILE(SMStext):
    print SMStext
    namefile = ''
    #for simplicity we use : before the name of the file

    IdUpdStr = SMStext.find(': ')
    if (IdUpdStr == -1 ):
        print 'no find Update string'
        return namefile

    PYfind = SMStext.find('.py')
    if(PYfind == -1) :
        print 'no find .PY ext'
        return namefile

    namefile = SMStext[IdUpdStr+2 : PYfind+3]
    return namefile

def GetFTP( ) :
    print 'configure PDP context with APN' +GPRS_APN+ ', username' + GPRS_USER
    time.sleep(10)
    print 'AT+CGDCONT=1,"IP","' + GPRS_APN + '"'
    res = MDM.send('AT+CGDCONT=1,"IP","' + GPRS_APN + '"\r', 2)
    res = MDM_waitfor('OK',20)
    if (res == -1):
        print 'error setting PDP context\r'
        return res

    print 'activate GPRS context\r'
    res = MDM.send('AT#GPRS=1\r',2)
    res = MDM_waitfor('OK',20)
    if (res == -1):
        print 'error activating GPRS'
        return res
	
    print 'all settings done\r'
    #s=''
    print 'open ftp\r'

    print 'AT#FTPOPEN="' + FTPSERVER_ADDR + '","' + FTPUSERNAME + '","' + FTPPASSWORD + '",0'
    
    a = MDM.send('AT#FTPOPEN="' + FTPSERVER_ADDR + '","' + FTPUSERNAME + '","' + FTPPASSWORD + '",0\r', 5)
    res = MDM_waitfor('OK',50)
    print res
    if (res == -1):
        print 'error OPENING FTP server'
        return res
    else:
        print 'ok FTP open'

    time.sleep(5)
    a = MDM.send('AT#FTPTYPE=0\r', 0)
    res = MDM_waitfor('OK',20)
    if(res == -1):
        print 'error SETTING FTP type'
        return res

    return 1



def savefile(data,filename):

    print 'save file'
    enddata = data[-DISC_LEN:]
    
    fNoCarrier = enddata.find('NO CARRIER')
    print 'fNoCarrier: ' + str(fNoCarrier)
    if(fNoCarrier == -1):
        print 'no carrier NOT present'
        FileSize = len(data)
    else:
        print 'no carrier  present'
        lentoCut = DISC_LEN - fNoCarrier
        FileSize = len(data)  - lentoCut
        
        
    print FileSize
    datatosave = data[:FileSize]
    print datatosave
    checkdata = datatosave[:30]
    res = checkdata.find('CONNECT')
    print res
    if(res != -1):
        print 'found connect'
        datatosave = data[res+START_LEN:FileSize]
        print datatosave
        
    myfile = '/sys/' + filename
    print myfile
    print 'open file'
    f = open(myfile, "w")
    f.write(datatosave)
    f.close()
    print 'file wrote and closed'
    return 1


def GetFTPFile(filename):

    strget = 'AT#FTPGET="' + filename + '"\r'
    print strget
    a = MDM.send(strget, 0 )
    data = ''

    time.sleep(5)
    timer = time.time()
    timeout = timer + 30 #secondi

    print 'start while'
    while(( MDM.getDCD() != 0) and (timer < timeout)):
        #print 'dentro while'
        data = data + MDM.read()
        #print data
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
        
    time.sleep(10)
    if MDM.getDCD() == 1:
        print 'connected'
        time.sleep(10)
        print 'disconnect'
        MDM.send('+++',10)
        time.sleep(10)
        myret = MDM_receive(50)
        print myret
    else:
        print 'DCD not active'

        
    print 'FTP close'
    a = MDM.send('AT#FTPCLOSE\r', 5)
    ret = MDM_receive(50)
    print ret

    print 'deactivate GPRS'
    res = MDM.send('AT#GPRS=0\r',2)
    res = MDM_waitfor('OK',20)
    if (res == -1):
        print 'error deactivating GPRS'
        #return -1

    print 'done'
    print 'save file'
    saved = savefile(data,filename)

    return 1


def enablefile(filename):
    escriptfile = 'AT#ESCRIPT="' + filename + '"\r'
    print escriptfile
    res = MDM.send( escriptfile,0 )
    res = MDM_waitfor('OK',20)
    if (res == -1):
        print 'error enabling the script'
        return -1
    else:
        print 'ok'
        return 1

    
    

def Main(out_string):

    FILENAME = ''
    telnumb = ''
    SmsSetup()
    MDMdata = ''
    timerCount = 12
    SMSindex = -1
    okdownl = 0
    while 1:
        MDMdata=''
        print  'mydata'

        while 1:
            MDMdata = MDM_receiveUntil('+CMTI:',10)
            print out_string
            print MDMdata
            if(MDMdata != ''):
                break
            timerCount = timerCount -1
            if(timerCount == 0):
                print 'counter to zero exit'
                break

        strSmsindex = findSmsPos(MDMdata)
        if(strSmsindex != ''):
            SMSindex = int(strSmsindex)


        print 'ecco sms index'
        print SMSindex
        if  (SMSindex != -1):
            cmgr = 'AT+CMGR=' + str(SMSindex) + '\r'
            print cmgr
            a = MDM.send(cmgr, 0)
            # ... parse it to determine if it's announcing an update ...
            SMStext = MDM_receiveUntil('OK',10)
            print SMStext
            TxtSMS = LookforSMS(SMStext)
            print TxtSMS
            if(TxtSMS != ''):
                print 'extrating NUM from recived SMS->'
                telnumb = ExtraxtNUM(SMStext,'+CMGR: "REC UNREAD"')
                print 'OK get the file name'
                FILENAME = ExtraxtNAMEFILE(TxtSMS)
                print 'filename:'
                print FILENAME

                if(FILENAME == ''):
                    print 'UPDATE SMS has NO FILE NAME: UPDATE PROCEDURE FAILED!'
                    okdownl = 0
                    delsms(SMSindex)
                    timerCount = 0
                    return -1
                else:
                    print 'open ftp connection'
                    okdownl = 1

                    if( okdownl == 1):
                        res = GetFTP()
                        if(res == -1):
                            txt = 'Error opening FTP : UPDATE PROCEDURE FAILED!!!!'
                            print txt
                            res = sendsms(telnumb,txt)
                            if(res == -1):
                                print 'error sending sms'
                            return -1

                        ret = GetFTPFile( FILENAME )

                        if(ret == -1):
                            txt = 'error getting file : UPDATE PROCEDURE FAILED!!!!'
                            print txt
                            res = sendsms(telnumb,txt)
                            if(res == -1):
                                print 'error sending sms'
                            return -1

                        ret = enablefile( FILENAME )
                        if(ret == -1):
                            txt = 'error enabling the file: UPDATE PROCEDURE FAILED!!!!'
                            print txt
                            res = sendsms(telnumb,txt)
                            if(res == -1):
                                print 'error sending sms'
                            return -1
                            
                        txt = 'SCRIPT SAVED AND  ENABLED REBOOT THE SYSTEM'
                        print txt
                        res = sendsms(telnumb,txt)
                        if(res == -1):
                            print 'error sending sms'
                        
                        time.sleep(20)
                        
                        print '-----> REBOOTING SYSTEM'
                        res = MDM.send('AT#REBOOT\r', 0)
                        
                              
            #print 'deleting SMS->'
            #delsms(SMSindex)
            #time.sleep(10)

            return 1

        else:
            print 'NO UPDATE SMS'
            print 'deleting SMS->'
            delsms(SMSindex)
            timerCount = 0
            return -1

    return 0
                
out_string = 'Update over the air demo, before to be updated'
Main(out_string)
