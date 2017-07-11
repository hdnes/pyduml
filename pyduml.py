#!/usr/bin/python
# HDnes pythonDUML
# Thanks the_lord for the sniffing
import os

from table_crc import *
import struct
import hashlib

# Enter upgrade mode (delete old file if exists)
packet_1 = bytearray.fromhex(u'55 16 04 FC 2A 28 65 57 40 00 07 00 00 00 00 00 00 00 00 00 27 D3')
# Enable Reporting
packet_2 = bytearray.fromhex(u'55 0E 04 66 2A 28 68 57 40 00 0C 00 88 20')

# ToDo: Send packets 1,2 above via pyusb raw packet transfer
# ToDo: put ftp file transfer here! /ftp/upgrade/xxx_system.bin

# 551A04B12A286B5740000800YYYYYYYY0000000000000204XXXX
#YYYYYYYY - file size in little endian
#XXXX - CRC as produced by dji_crc.py

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/fireworks.tar"
# Pack file size into 4 byte Long little endian
file_size = struct.pack('<L',int(os.path.getsize(dir_path)))

packet_3 = bytearray.fromhex(u'55 1A 04 B1 2A 28 6B 57 40 00 08 00')
packet_3 += file_size #append file size
packet_3 += bytearray.fromhex(u'00 00 00 00 00 00 02 04')
#print ' '.join(format(x, '02X') for x in packet_3)

packet_length = len(packet_3)
crc = calc_checksum(packet_3,packet_length)
#print "%02X %02X" % (crc & 0xFF, crc >> 8)
crc = struct.pack('<H',crc)
packet_3 += crc
print ' '.join(format(x, '02X') for x in packet_3)


# Calculate File md5 hash
filehash = hashlib.md5()
filehash.update(open(dir_path).read())
filehash = filehash.hexdigest()
hex_data = filehash.decode("hex")
md5_check = bytearray(hex_data)
print ' '.join(format(x, '02X') for x in md5_check)


# File Verification and Start Upgrade
packet_4 = bytearray.fromhex(u'55 1E 04 8A 2A 28 F6 57 40 00 0A 00')
packet_4 += md5_check

packet_length = len(packet_4)
crc = calc_checksum(packet_4,packet_length)
#print "%02X %02X" % (crc & 0xFF, crc >> 8)
crc = struct.pack('<H',crc) #need to check endianess?
packet_4 += crc
print ' '.join(format(x, '02X') for x in packet_4)

# ToDo: Send packet 3,4 via pyusb raw packet transfer


