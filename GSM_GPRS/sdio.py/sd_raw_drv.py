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
# Partial port from original code:
# Copyright (c) 2006-2009 by Roland Riegel <http://www.roland-riegel.de>
########################################################################

"""
sd_raw_drv.py
Implements Telit Python SD card raw SPI IO driver.
16/12/09 First version.
"""

import GPIO
import SPI
import sd_defs

# get driver version
def get_drv_version():
    return sd_defs.version

# set driver logging 1:enable, 0:disable
def set_logging(val):
    sd_defs.log = val

# driver logging implementation
def do_log(msg):
    if (sd_defs.log == 1):
        print msg

# SPI bus and SD card initialization 
def sd_initialize(SCLK, MOSI, MISO, SS):
    do_log("Start card initialization\r\n")    
    sd_defs.sdcard = SPI.new(SCLK, MOSI, MISO)
    sd_defs.SS = SS
    ret = sd_defs.sdcard.init(0, 0)
    if (ret == -1):
        do_log("Cannot init SPI bus\r\n") 
        return -1
    if (sd_raw_init() == -1):
        do_log("Cannot init card\r\n") 
        return -1

# SD card initialization
def sd_raw_init():
    unselect_card()
    # card needs 74 cycles minimum to start up
    for i in range(10):
        sd_raw_send_byte(0xFF)
    select_card()
    # reset card
    i = 0
    while (1 == 1):
        do_log("Send cmd: CMD_GO_IDLE_STATE\r\n")
        response = sd_raw_send_command(sd_defs.CMD_GO_IDLE_STATE, 0)
        do_log("Answer: %d\r\n" % response)
        if (response == (1 << sd_defs.R1_IDLE_STATE)):
            break
        i = i + 1;
        if (i == 0x1ff):
            do_log("Cannot RESET card\r\n")
            unselect_card()
            return -1
    do_log("Card RESET succedded\r\n")
       
    # determine SD/MMC card type
    do_log("Send cmd: CMD_APP\r\n")
    sd_raw_send_command(sd_defs.CMD_APP, 0)
    do_log("Send cmd: CMD_SD_SEND_OP_COND\r\n")
    response = sd_raw_send_command(sd_defs.CMD_SD_SEND_OP_COND, 0)
    do_log("Answer: %d\r\n" % response)
    if ((response & (1 << sd_defs.R1_ILL_COMMAND)) == 0):
        #card conforms to SD 1 card specification
        sd_defs.sd_raw_card_type = sd_defs.sd_raw_card_type | (1 << sd_defs.SD_RAW_SPEC_1)
        do_log("Card conforms with SD 1\r\n")
    else:
        # MMC card
        do_log("MMC card\r\n")
        # we don't support MMC cards
        unselect_card()
        return -1

    # wait for card to get ready
    k = 0
    while (1 == 1):
        if (sd_defs.sd_raw_card_type & ((1 << sd_defs.SD_RAW_SPEC_1) | (1 << sd_defs.SD_RAW_SPEC_2))):
            arg = 0
            do_log("Send cmd: CMD_APP\r\n")
            sd_raw_send_command(sd_defs.CMD_APP, 0)
            do_log("Send cmd: CMD_SD_SEND_OP_COND\r\n")
            response = sd_raw_send_command(sd_defs.CMD_SD_SEND_OP_COND, arg)
            do_log("Answer: %d\r\n" % response)
        else:
            do_log("Send cmd: CMD_SEND_OP_COND\r\n")
            response = sd_raw_send_command(sd_defs.CMD_SEND_OP_COND, 0)
            do_log("Answer: %d\r\n" % response)
        if ((response & (1 << sd_defs.R1_IDLE_STATE)) == 0):
            do_log("Card READY\r\n")
            break
        k = k + 1
        if (k == 0x7FF):
            unselect_card()
            do_log("Cannot get card READY\r\n")
            return -1
    # set block size
    do_log("Send cmd: CMD_SET_BLOCKLEN, size %d\r\n" % sd_defs.block_size)
    response = sd_raw_send_command(sd_defs.CMD_SET_BLOCKLEN, sd_defs.block_size)
    do_log("Answer: %d\r\n" % response)
    if (response):
        unselect_card()
        do_log("Cannot set block size\r\n")
        return -1
    unselect_card()
    return 1

# unselect SD card
def unselect_card():
    # SS low
    GPIO.setIOvalue(sd_defs.SS,1)

# select SD card
def select_card():
    # SS low
    GPIO.setIOvalue(sd_defs.SS,0)

# send byte on SPI bus
def sd_raw_send_byte(b):
    sd_defs.sdcard.sendbyte(b)

# receive byte on SPI bus
def sd_raw_rec_byte():
    ret = sd_defs.sdcard.readbyte()
    return ret

# send SD card command
def sd_raw_send_command(command, arg):
    # wait some clock cycles
    sd_raw_send_byte(0xFF)

    # send command via SPI
    sd_raw_send_byte(0x40 | command)
    sd_raw_send_byte((arg >> 24) & 0xff)
    sd_raw_send_byte((arg >> 16) & 0xff)
    sd_raw_send_byte((arg >> 8) & 0xff)
    sd_raw_send_byte((arg >> 0) & 0xff)
    if (command == sd_defs.CMD_GO_IDLE_STATE):
        sd_raw_send_byte(0x95)
    elif (command == sd_defs.CMD_SEND_IF_COND):
        sd_raw_send_byte(0x87)
    else:
        sd_raw_send_byte(0xff)
    sd_raw_send_byte(0xff)
    
    # receive response
    for i in range(10):
        response = sd_raw_rec_byte()
        if (response != 0xFF):
            break

    return response

# get SD card info from CSD and CID registers
def sd_raw_get_info():
    select_card()
    
    do_log("Send cmd: CMD_SEND_CID\r\n")
    response = sd_raw_send_command(sd_defs.CMD_SEND_CID, 0)
    do_log("Answer: %d\r\n" % response)
    if (response):
        unselect_card()
        return -1
    
    result = sd_raw_rec_byte()
    while (result != 0xFE):
        result = sd_raw_rec_byte()
    
    do_log("Start getting info values\r\n")
    for i in range(18):
        b = sd_raw_rec_byte()
        if (i == 0):
            sd_defs.sd_raw_info["manufacturer"] = b
            do_log("manufacturer %d\r\n" % sd_defs.sd_raw_info["manufacturer"])
        elif (i == 2):
            sd_defs.sd_raw_info["oem"] = b
            do_log("oem %s\r\n" % sd_defs.sd_raw_info["oem"])
        elif (i == 7):
            sd_defs.sd_raw_info["product"] = b
            do_log("product %s\r\n" % sd_defs.sd_raw_info["product"])
        elif (i == 8):
            sd_defs.sd_raw_info["revision"] = b
            do_log("revision %d\r\n" % sd_defs.sd_raw_info["revision"])
        elif (i == 12):
            sd_defs.sd_raw_info["serial"] = sd_defs.sd_raw_info["serial"] | (b << ((12 - i) * 8))
            do_log("serial %d\r\n" % sd_defs.sd_raw_info["serial"])
        elif (i == 13):
            sd_defs.sd_raw_info["manufacturing_year"] = b << 4
        elif (i == 14):
            sd_defs.sd_raw_info["manufacturing_year"] = sd_defs.sd_raw_info["manufacturing_year"] | (b >> 4)
            do_log("manufacturing_year %d\r\n" % sd_defs.sd_raw_info["manufacturing_year"])
            sd_defs.sd_raw_info["manufacturing_month"] = b & 0x0F
            do_log("manufacturing_month %d\r\n" % sd_defs.sd_raw_info["manufacturing_month"])

    do_log("Send cmd: CMD_SEND_CSD\r\n")
    response = sd_raw_send_command(sd_defs.CMD_SEND_CSD, 0)
    do_log("Answer: %d\r\n" % response)
    if(response):
        unselect_card()
        return -1

    result = sd_raw_rec_byte()
    while (result != 0xFE):
        result = sd_raw_rec_byte()

    for i in range(18):
        b = sd_raw_rec_byte()
        if (i == 14):
            if (b & 0x40):
                sd_defs.sd_raw_info["flag_copy"] = 1
            if (b & 0x20):
                sd_defs.sd_raw_info["flag_write_protect"] = 1
            if (b & 0x10):
                sd_defs.sd_raw_info["flag_write_protect_temp"] = 1
            sd_defs.sd_raw_info["format"] = (b & 0x0c) >> 2
        elif (i == 5):
            csd_read_bl_len = b & 0x0f
        elif (i == 6):
            csd_c_size = b & 0x03
            csd_c_size = csd_c_size << 8
        elif (i == 7):
            csd_c_size = csd_c_size | b
            csd_c_size = csd_c_size << 2
        elif (i == 8):
            csd_c_size = csd_c_size | ( b >> 6)
            ++csd_c_size
        elif (i == 9):
            csd_c_size_mult = b & 0x03
            csd_c_size_mult =  csd_c_size_mult << 1
        elif (i == 10):
            csd_c_size_mult = csd_c_size_mult | (b >> 7)
            sd_defs.sd_raw_info["capacity"] = csd_c_size << (csd_c_size_mult + csd_read_bl_len + 2)
            do_log("Capacity: %d\r\n" % sd_defs.sd_raw_info["capacity"])

    unselect_card()
    return 1

# read data from SD card
def sd_raw_read(offset, length):
    block_address = 0
    block_offset = 0
    read_length = 0
    buff = ""
    
    while (length > 0):
        # determine byte count to read at once
        block_offset = offset % sd_defs.block_size
        block_address = offset - block_offset
        read_length = sd_defs.block_size - block_offset        # read up to block border
        if (read_length > length):
            read_length = length
        
        select_card()
        
        for i in range(5):
            do_log("Send cmd: CMD_READ_SINGLE_BLOCK block addr %d\r\n" % block_address)
            response = sd_raw_send_command(sd_defs.CMD_READ_SINGLE_BLOCK, block_address)
            do_log("Answer: %d\r\n" % response)
            if (response == 0):
                break
        if (response):
            unselect_card()
            return -1
        result = sd_raw_rec_byte()
        while (result != 0xFE):
            result = sd_raw_rec_byte()
            
        # read byte block
        added = 0
        for i in range(sd_defs.block_size):
            ret = chr(sd_raw_rec_byte())
            if ((added < read_length) and (i >= block_offset)):
                buff = buff + ret
                added = added + 1
        
        # read crc16
        sd_raw_rec_byte()
        sd_raw_rec_byte()
        unselect_card()
        # let card some time to finish
        sd_raw_rec_byte()
        
        length = length - read_length
        offset = offset + read_length

    return buff    

# write data on SD card
def sd_raw_write(offset, buf):
    length = len(buf)
    block_address = 0
    block_offset = 0
    write_length = 0
    consumed = 0
    
    while (length > 0):
        # determine byte count to write at once
        block_offset = offset % sd_defs.block_size
        block_address = offset - block_offset
        write_length = sd_defs.block_size - block_offset # write up to block border
        if (write_length > length):
            write_length = length

        if ((block_offset == 0) and (write_length == sd_defs.block_size)):
            # write entire block, no need to read the original first
            select_card()
            for i in range(5):
                do_log("Send cmd: CMD_WRITE_SINGLE_BLOCK block addr %d\r\n" % block_address)
                response = sd_raw_send_command(sd_defs.CMD_WRITE_SINGLE_BLOCK, block_address)
                do_log("Answer: %d\r\n" % response)
                if (response == 0):
                    break
            if (response):
                unselect_card()
                return -1

            # send start byte
            sd_raw_send_byte(0xFE)
    
            for i in range(sd_defs.block_size):
                sd_raw_send_byte(ord(buf[consumed]))    
                consumed = consumed + 1    
        else:
            # write partial block, need to read the original first
            block = sd_raw_read(block_address, sd_defs.block_size)
            if (block == -1):
                return -1
            
            towrite = ""
            for i in range(sd_defs.block_size):
                if (i < block_offset):
                    towrite = towrite + block[i]
                else:
                    if (i - block_offset  < length):
                        towrite = towrite + buf[consumed]
                        consumed = consumed + 1
                    else:
                        towrite = towrite + block[i]                    
            
            select_card()
            for i in range(5):
                do_log("Send cmd: CMD_WRITE_SINGLE_BLOCK block addr %d\r\n" % block_address)
                response = sd_raw_send_command(sd_defs.CMD_WRITE_SINGLE_BLOCK, block_address)
                do_log("Answer: %d\r\n" % response)
                if (response == 0):
                    break
            if (response):
                unselect_card()
                return -1

            # send start byte
            sd_raw_send_byte(0xFE)
    
            for i in range(sd_defs.block_size):
                sd_raw_send_byte(ord(towrite[i]))

        # write dummy crc16
        sd_raw_send_byte(0xFF)
        sd_raw_send_byte(0xFF)

        # wait while card is busy
        k = 0
        while (k < 20):
            if (sd_raw_rec_byte() == 0xFF):
                k = k + 1

        unselect_card()
        
        offset = offset + write_length
        length = length - write_length

    return 1

