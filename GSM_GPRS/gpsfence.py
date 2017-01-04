import MDM
import SER
import MOD #import the built-in modules MOD

GPS_Data_Quality = ''
Sat_Num = ''
Time_Date = ''
Speed_str = ''
Dir = ''
Lats = ''
Lons = ''
BaseLat = ''
BaseLon = ''

FENCE_RADIUS = 50

TEL_NUMBER = '1111111111'  # to be changed


def Debugging(temp):
    res1 =  temp +'\r\n'          
    SER.send("%s" % res1)       


# waiting function
def Wait(sec):
    timer = MOD.secCounter()
    timerstop = timer + sec
    while timer < timerstop:
        timer = MOD.secCounter()

def MDM_receive(timeout):
    res = ''
    start = MOD.secCounter()
    while (MOD.secCounter() - start < timeout):
        res = res + MDM.read()
    return res

def MDM_waitfor(value, timeout):
    res = ''
    found = -1
    start = MOD.secCounter()
    while (MOD.secCounter() - start < timeout):
        res = res + MDM.read()
        found = res.find(value)
        if(found != -1):
            return found
        
    return found

def MDM_receiveUntil(value,timeout):
    res = ''
    found = -1
    start = MOD.secCounter()
    while (MOD.secCounter() - start < timeout):
        res = res + MDM.read()
        found = res.find(value)
        if(found != -1):
            return res
            
    return res


def SmsSetup():
    
    a = MDM.send('AT+CMGF=1\r', 0)
    print 'AT+CMGF=1\r'
    Debugging('AT+CMGF=1')
    trovato = MDM_waitfor('OK', 10)
    print trovato
    a = MDM.send('AT+CNMI=2,1\r', 0)
    print 'AT+CNMI=2,1\r'
    Debugging('AT+CMGF=1')
    trovato = MDM_waitfor('OK', 10)
    print trovato

def sendsms(NUM,TEXT):
    res = MDM.send('AT+CMGS=', 0)
    res = MDM.send(NUM, 0)
    res = MDM.sendbyte(0x0d, 0)
    res = MDM_receiveUntil('>',10)
    if(res == -1):
        Debugging('error sending sms')
        print 'error sending sms'
        MDM.sendbyte(0x1b,0)
        return -1
        
    res = MDM.send(TEXT, 0)
    res = MDM.send('\x1a', 0)
    Debugging('sending sms ...')
    print 'sending sms ...'
    return 1

def GPSon():
    MDM.send('AT$GPSP=1\r',0)
    Debugging('AT$GPSP=1')
    print 'AT$GPSP=1\r'
    trovato = MDM_waitfor('OK', 10)
    print trovato
    if(trovato == -1):
        Debugging('error setting AT$GPSP=1')

def DivByZeroSix(In_minutes) :                                     
    try:
        return (In_minutes * 10) / 6
    except:
        return 0

def MultBigNums(a,b) :
    try:
        a_hi = a/10000
        a_low = a%10000
        b_hi = b/10000
        b_low = b%10000
        return(a_hi * b_hi + a_hi * b_low / 10000 + a_low * b_hi / 10000 + a_low * b_low / 100000000)
    except:
        return (0)

def SqrRootCalculate(temp):
    res = 1                                        
    res1 = temp                                 
    try:        
        while abs(res1 - res)>1:             # While Second Root > First Root
            res = abs(temp/res1)        # Divide input num by smaller Root
            res1 = abs(res1 + res)/2    

        return res1    
    except:
        Debugging('error  SqrRootCalculate()')
        return 0


def MultByCosine(dif_angle,angle) :
    try:
        if angle < 13000000:
            return(dif_angle)
        elif angle > 13000000 and angle < 32000000 :
            return(dif_angle * 9 / 10)
        elif angle > 32000000 and angle < 42000000 :
            return(dif_angle * 8 / 10)
        elif angle > 42000000 and angle < 50000000 :
            return(dif_angle * 7 / 10)
        elif angle > 50000000 and angle < 57000000 :
            return(dif_angle * 6 / 10)
        elif angle > 57000000 and angle < 63000000 :
            return(dif_angle * 5 / 10)
        elif angle > 63000000 and angle < 70000000 :
            return(dif_angle * 4 / 10)
        elif angle > 70000000 :
            return(dif_angle * 3 / 10)   
    except :
        return(0)

def reproject(latitude, longitude):
    earth_radius = 6371009 # in meters
    pi = 31415927

    temp = MultBigNums(earth_radius,pi)
    lat_dist = (temp * 100)/18
    LatMeterDistance = MultBigNums(lat_dist,latitude)
    
    long_dist = MultByCosine(longitude,latitude)
    LonMeterDistance = MultBigNums(lat_dist, long_dist)

    return LatMeterDistance, LonMeterDistance



def diffLatLon(newlat, newlon, latbase, lonbase):

    Debugging('newlat: ' + newlat)
    Debugging('newlon: ' + newlon)
    Debugging('latbase: ' + latbase)
    Debugging('lonbase: ' + lonbase)
    intNlat = int(newlat)
    intNlon = int(newlon)
    intlatbase = int(latbase)
    intlonbase = int(lonbase)

    print intNlat
    print intNlon
    print intlatbase
    print intlonbase
 
    NordSud = newlat[0]
    baseNordSud = latbase[0]

    EstOvest = newlon[0]
    baseEstOvest = lonbase[0]

    print 'value nord sud newlat: ' +NordSud+ ' latbase: '+baseNordSud+ 'value est ovest newlon: ' +EstOvest+ 'lonbase: '+baseEstOvest
 
    meterlat, meterlon = reproject(intlatbase, intlonbase)

    print meterlat
    print meterlon

    meterNewlat, meterNewlon = reproject(intNlat, intNlon)
    
    print meterNewlat
    print meterNewlon
    

    if baseNordSud == NordSud :
        difflat = abs(meterNewlat - meterlat)
    else:
        difflat = abs(meterNewlat + meterlat)

    if baseEstOvest == EstOvest :
        difflon = abs(meterNewlon - meterlon)
    else:
        difflon = abs(meterNewlon + meterlon)

    Debugging('difflat: ' + str(difflat))
    Debugging('difflon: ' + str(difflon))
        
    sqrReferenceInt = difflat * difflat + difflon * difflon
    distance = SqrRootCalculate(sqrReferenceInt)

    Debugging('distance in meters: ' + str(distance))
    
    return distance



def GPSgetpos(GPSDataStr):
    
    Fieldstot = GPSDataStr.split('$GPSACP:')                     # Formatting input data by GPS to data array
    Fields = Fieldstot[1].split(',')                           # Get value in our protocol
    if Fields[10]!='':
        Sat_Num = Fields[10]
        Sat_Num = Sat_Num[0] + Sat_Num[1]                       # Get satellite's number value
        print Sat_Num
        Debugging('sat num: ' + Sat_Num)
        if Sat_Num == '' or int(Sat_Num)>12 or int(Sat_Num)<= 0:
            Sat_Num='00'

    if Fields[5]!='':
        GPS_Data_Quality = Fields[5]                                   # Get Data_Quality value
        print GPS_Data_Quality
        Debugging('GPS_Data_Quality: ' + GPS_Data_Quality)
        if GPS_Data_Quality == '2' or GPS_Data_Quality == '3' :
            GPS_Data_Quality = '01'     
        else  :
            GPS_Data_Quality = '00'

    if Fields[9]!='' and  Fields[0]!='':
        Time_Date = Fields[9] + Fields[0]
        print Time_Date
        Debugging('Time_Date: ' + Time_Date)
        Time_Date = Time_Date.split('.')
        Time_Date = Time_Date[0].split(' ')
        Time_Date = Time_Date[0] + Time_Date[1]           # Get Time/Date data
        print Time_Date

    if Fields[7]!='':
       Speed_str = Fields[7]                                 # Get speed 
       print Speed_str
       Debugging('Speed_str: ' + Speed_str)

    if Fields[6]!='':                        
        Dir = Fields[6]                 # Get direction value
        print Dir
        Debugging('direction: ' + Dir)

    if Fields[1]!='':                    
        Lats = Fields[1]
        print Lats
        Debugging('latitude: ' + Lats)
        
        Lats = Lats.split('.')
        res = Lats[0] + Lats[1]                        # Get Latitude value
        Lat_min_str = res[2:8]
        Debugging('Lat_min_str: ' + Lat_min_str)
        temp=0
        temp = int(Lat_min_str)                           # String's convertion to integer
        temp = DivByZeroSix(temp)                     # Call convert function from deviding by 60 to deviding by 100
        Lat_min_str = str(temp)                                     
        Debugging('Lat_min_str: ' + Lat_min_str)
        #temp=0
        Dif_Len_Lat_min_str = 6 - len(Lat_min_str)
        while Dif_Len_Lat_min_str :                                   # Appends zeros while has less from 6 digits 
            Lat_min_str = '0' + Lat_min_str
            Dif_Len_Lat_min_str = Dif_Len_Lat_min_str - 1
        if res[8] == 'S' :                                      # If Unit has South Position
            sign = '-'                                                #  sign is "-"
        else :                                                         # else    
            sign = '+'                                                 # sign is "+"
        valreslat = sign + res[0] + res[1] +  Lat_min_str         # Building longitude value
        Debugging('valreslat: ' + valreslat)



    if Fields[2]!='':  
        Lons = Fields[2]
        print Lons
        Debugging('longitude: ' + Lons)
        Lons = Lons.split('.')
        res =Lons[0] + Lons[1]                                          # Get longitude value
        Lon_min_str = res[3:9] 
        
        temp=0
        temp = int(Lon_min_str)                                      # String's convertion to integer
        temp = DivByZeroSix(temp)                             # Call convert function from deviding by 60 to deviding by 100
        Lon_min_str = str(temp)                                      # Integer's convertion to string
        temp=0
        temp = 6 - len(Lon_min_str)
        while temp :                                         # Appends zeros while has less from 6 digits 
            Lon_min_str = '0' + Lon_min_str
            temp = temp - 1
        if res[9] == 'W' :                                              # If Unit has West Position
            sign = '-'                                                      #  sign is "-"
        else :                                                                
            sign = '+'                                                      
        valreslon = sign + res[0] + res[1] + res[2] +  Lon_min_str   # Building longitude value
        Debugging('valreslon: ' + valreslon)

    return (valreslat,valreslon)


def Main(out_string):

    SER.set_speed('115200')
    Debugging(out_string)
    SmsSetup()
    Wait(2)
    GPSon()
    Wait(2)
    MDM.send('AT$GPSACP\r', 0)
    str_res = MDM_receiveUntil('OK',20)
    BaseLat, BaseLon =GPSgetpos(str_res)
    Wait(2)
    count = 70

    while count > 0:
        MDM.send('AT$GPSACP\r', 0)
        str_res = MDM_receiveUntil('OK',20)
        Lats,Lons = GPSgetpos(str_res)
        diff = diffLatLon(Lats,Lons,BaseLat,BaseLon)
        Debugging('diff: ' + str(diff))

        if diff > FENCE_RADIUS:
            Debugging('outside fence')
            sendsms(TEL_NUMBER, 'outside fence')
        else:
            Debugging( 'inside fence' )

            
        Wait(30)
        count = count -1
        Debugging('count: ' + str(count))
        
        
    
out_string = 'GPS fence demo'
Main(out_string)
Debugging('exit')
