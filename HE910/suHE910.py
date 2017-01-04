# import the built-in modules
import MDM
import SER
import time

#firtst set at#portcfg=3 and reboot the module in order to collect data on USIF1 

class Survey(object):
    listoperator = []
    operatorGSM = []
    operatorUTRAN = []
    atcopsGSMlist = []
    atcopsUTRANlist = []
    stateGSM = []
    stateUTRAM = []
    listGSMmonival = []
    listGSMdbm = []
    listUTRANmonival = []
    
    def __init__(self):
        print 'Survey!'
        self.listoperator = []

    def checkCops(self, strcop):
        foundOPB = -1
        foundCLB = -1
        goOn = 1
        temp = strcop
        temp2 = temp
        scomp = ''
        while (goOn == 1):
            temp = temp2
            foundOPB = temp.find('(')
            foundCLB = temp.find(')')
            if(foundOPB != -1 and foundCLB  != -1):
                scomp = temp[foundOPB:foundCLB+1]
                print scomp
                self.listoperator.append(scomp)
                temp2 = temp[foundCLB+2:]
                print temp2
            else:
                goOn = 0

    def MDM_receive(self,timeout):
        res = ''
        start = time.time()
        while (time.time() - start < timeout):
            res = res + MDM.read()
        return res

    def MDM_waitfor(self,value, timeout):
        res = ''
        found = -1
        start = time.time()
        while (time.time() - start < timeout):
            res = res + MDM.read()
            found = res.find(value)
            if(found != -1):
                return found
        
        return found

    def MDM_waitfor2(self,value,value2, timeout):
        res = ''
        found = -1
        found2 = -1
        start = time.time()
        while (time.time() - start < timeout):
            res = res + MDM.read()
            found = res.find(value)
            if(found != -1):
                print res
                return found

            found2 = res.find(value2)
            if(found2 != -1):
                print res
                return found2

        print res
        return found


    def MDM_receiveUntil(self,value,timeout):
        res = ''
        found = -1
        start = time.time()
        while (time.time() - start < timeout):
            res = res + MDM.read()
            found = res.find(value)
            if(found != -1):
                return res
            
        return res
    

    def Surv__start(self):
        starttime = time.clock()
        print 'start time:'
        print starttime
        MDM.send('AT+COPS=0\r', 0)
        print 'AT+COPS=0\r'
        trovato = self.MDM_waitfor('OK', 20)
        SER.send('AT+COPS=0\r')
        if(trovato != -1):
            print 'ok go on'
            SER.send('OK\r')
        else:
            print  'error'
            SER.send('ERROR\r')
            return 0

        a = MDM.send('AT+CREG=2\r', 0)
        print 'AT+CREG=2\r'
        trovato = self.MDM_waitfor('OK', 20)
        SER.send('AT+CREG=2\r')
        if(trovato != -1):
            print 'ok go on'
            SER.send('OK\r')
        else:
            print  'error'
            SER.send('ERROR')
            return 0

        print 'AT+WS46=25\r'
        MDM.send('AT+WS46=25\r', 0)
        trovato = self.MDM_waitfor('OK', 20)
        SER.send('AT+WS46=25\r')
        if(trovato != -1):
            print 'ok go on'
            SER.send('OK\r')
        else:
            print  'error'
            SER.send('ERROR\r')
            return 0

        MDM.send('"AT+COPS=2\r', 0)
        print 'AT+COPS=2\r'
        trovato = self.MDM_waitfor('+CREG: 0', 20)
        SER.send('AT+COPS=2\r')
        if(trovato != -1):
            print '+CREG: 0'
            print 'ok go on'
            SER.send('+CREG: 0\rOK\r')
        else:
            print  'error'
            SER.send('ERROR\r')
            return 0
        
        stoptime = time.clock()

        return (stoptime - starttime)


    def Cops_cellInfo(self):
        time.sleep(1)
        MDM.send('AT+COPS=?\r', 0)
        SER.send('AT+COPS=?\r')
        print 'at+cops=?'
        isfound = 0
        res = ''
        timeout = 150
        found = -1
        start = time.time()
        while (time.time() - start < timeout):
            res = res + MDM.read()
            found = res.find('OK')
            if(found != -1):
                print 'ok AT+COPS'
                isfound = 1
                break

        print res
        SER.send(res)
        SER.send('\r')

        if(isfound == 0):
            print 'error 1'
            SER.send('ERROR\r')
            return 0
        else:
            print 'go on'
            
        strCops = res
        foundOPB = -1
        foundCLB = -1
        goOn = 1
        temp = strCops
        temp2 = temp
        scomp = ''
        while (goOn == 1):
            temp = temp2
            foundOPB = temp.find('(')
            foundCLB = temp.find(')')
            if(foundOPB != -1 and foundCLB  != -1):
                scomp = temp[foundOPB:foundCLB+1]
                print scomp
                self.listoperator.append(scomp)
                temp2 = temp[foundCLB+2:]
                print temp2
            else:
                goOn = 0


        tempop = ''
        suboperator = []
        foundOPB = -1
        foundCLB = -1
        foundtmp = -1
        foundtmp2 = -1

        tmtype = ''

        for word in self.listoperator:
            foundOPB = word.find('"')
            print word
            print foundOPB
            if(foundOPB != -1):
                foundCLB = word[foundOPB+1:].find('"')
                print foundCLB
                if(foundCLB != -1):
                    tempop = word[foundOPB:foundOPB+1+foundCLB+1]
                    print tempop
                    state = word[foundOPB-2:foundOPB-1]
                    print 'value of state'
                    print state
                    foundtmp = word[foundOPB+foundCLB+2:].find('"')
                    print foundtmp
                    if(foundtmp != -1):
                        print 'found this'
                        print foundtmp
                        print word[foundOPB+foundCLB+2:]
                        print word[foundOPB+foundCLB+2+foundtmp:]
                        foundtmp2 = word[foundOPB+foundCLB+2+foundtmp+1:].find('"')
                        if(foundtmp2 != -1):
                            print "this is it..."
                            tmtype = word[foundOPB+foundCLB+2+foundtmp+foundtmp2+3:foundOPB+foundCLB+2+foundtmp+foundtmp2+4]
                            print tmtype
                            print foundtmp2
                            print 'end'

                            if(tmtype == '0'):
                                self.operatorGSM.append(tempop)
                                self.stateGSM.append(state)
                            elif(tmtype == '2'):
                                self.operatorUTRAN.append(tempop)
                                self.stateUTRAM.append(state)
                        

            
                    suboperator.append(tempop)

                    
        print self.operatorGSM
        print self.operatorUTRAN
        return len(suboperator)

    def GatherUTRANInfo(self):
        print 'AT+WS46=22\r'
        MDM.send('AT+WS46=22\r', 0)
        
        trovato = self.MDM_waitfor('OK', 10)
        SER.send('AT+WS46=22\r')
        if(trovato != -1):
            SER.send('OK\r')
            print 'ok go on'
        else:
            print  'error'
            SER.send('ERROR\r')
            return 0

        for oper in self.operatorUTRAN :
            rich = 'AT+COPS=1,0,' + oper
            self.atcopsUTRANlist.append(rich)
            print rich
    
        print self.atcopsUTRANlist
        i = 0

        for atcom in self.atcopsUTRANlist:
            print atcom
            stringa = atcom+'\r'
            MDM.send(stringa,0)

            retstr = '+CREG: ' + self.stateUTRAM[i] 
            print retstr
            trovato = self.MDM_waitfor2(retstr,'+CREG: 5',32)
            
            SER.send(stringa)
            if(trovato != -1):
                print 'ok go on'
            else:
                print  'error'
                

            time.sleep(1)
            print 'AT#MONI=0'
            MDM.send('AT#MONI=0\r',0)
            trovato = self.MDM_waitfor('OK', 10)
            
            if(trovato != -1):
                
                print 'ok go on'
            else:
                print  'error'
                
            time.sleep(1)
            print 'AT#MONI'
            MDM.send('AT#MONI\r',0)
            
            res = self.MDM_receiveUntil('OK',12) 
            print res
           
            posit = res.find('#MONI:')
            print posit
            founddbm = res[posit+1:].find('\n') 
            print founddbm
            tempstring1 =  res[posit+1+5:posit+1+founddbm-1]
            print tempstring1
            self.listUTRANmonival.append(tempstring1)

            time.sleep(1)
            print 'AT#MONI=3'
            MDM.send('AT#MONI=3\r',0)
    
            if(trovato != -1):
                #SER.send('OK\r')
                print 'ok go on'
            else:
                print  'error'
                #SER.send('ERROR\r')

            i = i + 1
            time.sleep(1)
            print 'AT#MONI'
            MDM.send('AT#MONI\r',0)
            #SER.send('AT#MONI\r')
            res = self.MDM_receiveUntil('OK',12)
            
            print res
            #SER.send(res)
            time.sleep(1)

        print self.listUTRANmonival

        return 1

    def GatherGSMInfo(self):
        MDM.send('"AT+COPS=2\r', 0)
        print 'AT+COPS=2\r'
        trovato = self.MDM_waitfor('OK', 20)
        SER.send('AT+COPS=2\r')
        if(trovato != -1):
            print 'ok go on'
            #SER.send('OK\r')
        else:
            print  'error'
            #SER.send('ERROR\r')
            return 0
        
        print 'AT+WS46=12\r'
        MDM.send('AT+WS46=12\r', 0)
        
        trovato = self.MDM_waitfor('OK', 10)
        SER.send('AT+WS46=12\r')
        if(trovato != -1):
            print 'ok go on'
        else:
            print  'error'
            return 0

        for oper in self.operatorGSM :
            rich = 'AT+COPS=1,0,' + oper
            self.atcopsGSMlist.append(rich)
            print rich

        print self.atcopsGSMlist

        i = 0
        
        for atcom in self.atcopsGSMlist:
            print atcom
            stringa = atcom+'\r'
            MDM.send(stringa,0)
            retstr = '+CREG: ' + self.stateGSM[i] 
            print retstr
            trovato = self.MDM_waitfor2(retstr,'+CREG: 5',25)   
           
            if(trovato != -1):
                #SER.send(retstr+'\r') #'+CREG: 1\rOK\r')
                print 'ok go on'
            else:
                print  'error'
                #SER.send('ERROR\r')

            print self.operatorGSM[i]
            time.sleep(1)
            i +=1
            MDM.send('AT#MONI=7\r',0)
            trovato = self.MDM_waitfor('OK', 10)
            #SER.send('AT#MONI=7\r')
            if(trovato != -1):
                #SER.send('OK\r')
                print 'ok go on'
            else:
                print  'error'
                #SER.send('ERROR\r')
            time.sleep(1)
            MDM.send('AT#MONI\r',0)
            #SER.send('AT#MONI\r')
            res = self.MDM_receiveUntil('OK',12)
            print res
            posit = res.find('#MONI:  S')
            print posit
            founddbm = res[posit+1:].find('\n') 
            print founddbm
            tempstring1 =  res[posit+1+5:posit+1+founddbm-1]
            print tempstring1
            self.listGSMmonival.append(tempstring1)

        print self.listGSMmonival

        for datav in self.listGSMmonival:
            founddbm = datav.find('dbm')
            print founddbm
            print datav[founddbm-4: founddbm]
            mydbm = datav[founddbm-4: founddbm].strip()
            print mydbm
            temp = int(mydbm)
            self.listGSMdbm.append(temp)


    def bubblesortgsm(self):
        max = len(self.listGSMmonival)
        supportstr = ''
        for n in range(0,max): #upper limit varies based on size of the list
            temp = 0
            for i in range(1, max): #keep this for bounds purposes
                temp = self.listGSMdbm[i]
                supportstr = self.listGSMmonival[i]
                if self.listGSMdbm[i] > self.listGSMdbm[i-1]:
                    self.listGSMdbm[i] = self.listGSMdbm[i-1]
                    self.listGSMdbm[i-1] = temp
                    self.listGSMmonival[i] = self.listGSMmonival[i-1]
                    self.listGSMmonival[i-1] = supportstr
        
            

    def printSERgsm(self):
        SER.send('\rGSM survey:\r\r')
        strintro = ' Cell BSIC  LAC   CellId   ARFCN  Power    C1  C2  TA   RxQual     PLMN\r'
        SER.send(strintro)
        for valuemoni in self.listGSMmonival:
            SER.send(valuemoni+'\r')

        SER.send('\rGSM survey End\r\r')


    def printSERutram(self):
        SER.send('\rUMTS survey:\r\r')

        for valuemoni in self.listUTRANmonival:
            SER.send(valuemoni+'\r')
        
        SER.send('\rUMTS survey End\r\r')
        


a = Survey()
ret = a.Surv__start()
print 'return value for survey:'
print ret
ret = a.Cops_cellInfo()
print ret

SER.send('\rSTART\r')
SER.send('GATHERING GSM CELL INFORMATION:\r')
SER.send(str(a.operatorGSM))
SER.send('\r\r')
a.GatherGSMInfo()
a.bubblesortgsm()
a.printSERgsm()
SER.send('GATHERING UMTS CELL INFORMATION:\r')
SER.send(str(a.operatorUTRAN))
SER.send('\r\r')
a.GatherUTRANInfo()
a.printSERutram()


