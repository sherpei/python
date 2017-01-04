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
main.py
Part of sdio application, test for SD card Telit Python driver.
Performs SPI bus and SD card initialization, writes and reads some data.
16/12/09 First version.
"""

import sd_raw_drv
import sd_defs
import MOD

def test(SCLK,MOSI,MISO,SS):
    # Initialize SPI bus and SD card (SCLK, MOSI, MISO, SS, SD block size )
    print "Init SD card\r\n"
    if (sd_raw_drv.sd_initialize(SCLK,MOSI,MISO,SS) == -1):
        print "Failed to initialize SD card\r\n"
        return
    # Get card info
    print "Get SD card info\r\n"
    if (sd_raw_drv.sd_raw_get_info() == -1):
        print "Failed to get SD card info\r\n"
        return
    print "SD card capacity:", sd_defs.sd_raw_info["capacity"], " bytes\r\n"
    
    # builds a long string with 0123456789 pattern
    print "Build test string\r\n"
    a = ""
    k = 0
    for i in range(1380):
        a = a + chr(48 + k)
        k = k + 1
        if (k == 10):
            k = 0
 
    # writes the string on SD card 
    print "Write test string on SD card\r\n"
    res = sd_raw_drv.sd_raw_write(33415, a)
    print "Result: %d\r\n" % res 

    # reads the string back for verification
    print "Read back test string from SD card\r\n"
    res = sd_raw_drv.sd_raw_read(33400, 2000)
    print res, "\r\nString length: ", len(res), "\r\n"


    
    