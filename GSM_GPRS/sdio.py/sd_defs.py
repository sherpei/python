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
sd_defs.py
Part of Telit Python SD card raw SPI IO driver.
Global variables and SD card defines.
16/12/09 First version.
"""

# Driver version.
version = "20091216.1"
# Set 1 to print driver messages
log = 0

sdcard = None
SS = 0
block_size = 512

# CMD0: response R1
CMD_GO_IDLE_STATE = 0x00
# CMD1: response R1
CMD_SEND_OP_COND =  0x01
# CMD8: response R7
CMD_SEND_IF_COND = 0x08
# CMD9: response R1
CMD_SEND_CSD = 0x09
# CMD10: response R1
CMD_SEND_CID = 0x0a
# CMD17: arg0[31:0]: data address, response R1
CMD_READ_SINGLE_BLOCK = 0x11
# CMD16: arg0[31:0]: block length, response R1
CMD_SET_BLOCKLEN = 0x10
# CMD24: arg0[31:0]: data address, response R1
CMD_WRITE_SINGLE_BLOCK = 0x18
# ACMD41: arg0[31:0]: OCR contents, response R1
CMD_SD_SEND_OP_COND = 0x29
# CMD55: arg0[31:0]: stuff bits, response R1
CMD_APP = 0x37
# CMD58: arg0[31:0]: stuff bits, response R3
CMD_READ_OCR = 0x3a

# R1: size 1 byte
R1_IDLE_STATE = 0
R1_ILL_COMMAND = 2

# status bits for card types
SD_RAW_SPEC_1 = 0
SD_RAW_SPEC_2 = 1
SD_RAW_SPEC_SDHC = 2

sd_raw_card_type = 0

# SD card info, filled from cards's CSD and CID registers
sd_raw_info = {
            # A manufacturer code globally assigned by the SD card organization.
            "manufacturer" : 0,
            # A string describing the card's OEM or content, globally assigned by the SD card organization.
            "oem" : "",
            # A product name.
            "product" : "",
            # The card's revision, coded in packed BCD.
            # For example, the revision value \c 0x32 means "3.2".
            "revision" : 0,
            # A serial number assigned by the manufacturer.
            "serial" : 0,
            # The year of manufacturing. A value of zero means year 2000.
            "manufacturing_year" : 0,
            # The month of manufacturing.
            "manufacturing_month" : 0,
            # The card's total capacity in bytes.
            "capacity" : 0,
            # Defines wether the card's content is original or copied.
            # A value of \c 0 means original, \c 1 means copied.
            "flag_copy" : 0,
            # Defines wether the card's content is write-protected.
            # This is an internal flag and does not represent the
            # state of the card's mechanical write-protect switch.
            "flag_write_protect" : 0,
            # Defines wether the card's content is temporarily write-protected.
            # This is an internal flag and does not represent the
            # state of the card's mechanical write-protect switch.
            "flag_write_protect_temp" : 0,
            # The card's data layout.
            # See the \c SD_RAW_FORMAT_* constants for details.
            # This value is not guaranteed to match reality.
            "format" : 0
            }
