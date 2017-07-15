#!/usr/bin/python
# HDnes pythonDUML
# Thanks the_lord for the sniffing
# Thanks jaydee for the usb and ftp work

import time
import os
import sys
import serial
import usb.core
import usb.util
import struct
import hashlib
from ftplib import FTP
from table_crc import *

# ToDo: Send packets 1,2 above via pyusb raw packet transfer
# ToDo: put ftp file transfer here! /ftp/upgrade/xxx_system.bin
# ToDo: Send packet 3,4 via pyusb raw packet transfer

def main():
    #probe_for_device()
    configure_usb()
    generate_update_packets()
    write_packet(packet_1) # Enter upgrade mode (delete old file if exists)	
    write_packet(packet_2) # Enable Reporting
    upload_binary()
    write_packet(packet_3) # Send File size
    write_packet(packet_4) # Send MD5 Hash for verification and Start Upgrade

    print ("Firmware Upload Complete")
    ser.close
    return

def probe_for_device():
    # find our drone
    sys.stdout.write('Info: Looking for USB connected and compatible aircraft...\n')
    dev = usb.core.find(idVendor=0x2ca3, idProduct=0x001f)  # mavic pro

    # connected?
    if dev is None:
        sys.stdout.write('Error: Unable to find compatible aircraft. Plug it in, power it up, and try again.\n\n')
        sys.exit(2)

    if dev.idVendor == 11427 and dev.idProduct == 31:
        sys.stdout.write('Info: DJI Mavic Pro found.\n')
        return

def configure_usb():
    #serial.tools.list_ports
    global ser
    ser = serial.Serial(sys.argv[1])
    ser.baudrate = 115200  
    #data_bits = 8  
    #stop_bits = 1  
    #parity = SerialPort::NONE
    return

def write_packet(data):		
    ser.write(data)     # write a string
    time.sleep(0.1)
    hexout = ' '.join(format(x, '02X') for x in data)
    print (hexout)  
    return

def upload_binary():
    from pathlib import Path

    my_file = Path("dji_system.bin")
    if my_file.is_file():
        from ftplib import FTP
        ftp = FTP("192.168.42.2", "Gimme", "DatROot!")
        fh = open("dji_system.bin", 'rb')
        ftp.storbinary('STOR /upgrade/dji_system.bin', fh)
        ftp.mkdir("/upgrade/.bin")
        fh.close()
    return	

def generate_update_packets():
    # Enter upgrade mode (delete old file if exists)
    global packet_1 
    global packet_2 
    global packet_3 
    global packet_4

    packet_1 = bytearray.fromhex(u'55 16 04 FC 2A 28 65 57 40 00 07 00 00 00 00 00 00 00 00 00 27 D3')
    # Enable Reporting
    packet_2 = bytearray.fromhex(u'55 0E 04 66 2A 28 68 57 40 00 0C 00 88 20')


    # 551A04B12A286B5740000800YYYYYYYY0000000000000204XXXX
    #YYYYYYYY - file size in little endian
    #XXXX - CRC as produced by table_crc.py

    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/dji_system.bin"
    # Pack file size into 4 byte Long little endian
    file_size = struct.pack('<L',int(os.path.getsize(dir_path)))

    packet_3 = bytearray.fromhex(u'55 1A 04 B1 2A 28 6B 57 40 00 08 00')
    packet_3 += file_size #append file size
    packet_3 += bytearray.fromhex(u'00 00 00 00 00 00 02 04')

    packet_length = len(packet_3)
    crc = calc_checksum(packet_3,packet_length)
    crc = struct.pack('<H',crc)
    packet_3 += crc


    # Calculate File md5 hash
    filehash = hashlib.md5()
    filehash.update(open(dir_path).read())
    filehash = filehash.hexdigest()
    hex_data = filehash.decode("hex")
    md5_check = bytearray(hex_data)


    # File Verification and Start Upgrade
    packet_4 = bytearray.fromhex(u'55 1E 04 8A 2A 28 F6 57 40 00 0A 00')
    packet_4 += md5_check

    packet_length = len(packet_4)
    crc = calc_checksum(packet_4,packet_length)
    crc = struct.pack('<H',crc)
    packet_4 += crc
    return



if __name__ == "__main__":
    main()
