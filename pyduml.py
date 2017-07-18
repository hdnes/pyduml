#!/usr/bin/python

# HDnes pythonDUML
# Thanks Hostile for the fireworks grepping all the fish.
# Thanks the_lord for the sniffing
# Thanks hfman & jaydee for the usb and ftp work
# Thanks vk2fro for UI selector,bin sourcing/managing, and auto connect

import time
import os
import sys
import serial
import usb.core
import usb.util
import struct
import hashlib
from table_crc import *
from pyduml_menu import *


def main():
   
    remove_stale_bin()
    probe_for_device()
    device = pyduml_UI()
    configure_usb()
    generate_update_packets(device)
    write_packet(packet_1) # Enter upgrade mode (delete old file if exists) 
    write_packet(packet_2) # Enable Reporting
    upload_binary()
    write_packet(packet_3) # Send File size
    write_packet(packet_4) # Send MD5 Hash for verification and Start Upgrade
    print ("--------------------------------------------------------------------------") 
    print ("Upgrade/Downgrade in Progress - May take a while....")
    ser.close
    return


def remove_stale_bin():

    if os.path.exists('./dji_system.bin')==True:
        print ("--------------------------------------------------------------------------")
        print ("removing stale dji_system.bin")
        print ("--------------------------------------------------------------------------")
        os.remove("dji_system.bin")

    return

def probe_for_device():
    global port

    os.system('ls /dev/tty* | sed -e "s#.*/##g" > /tmp/dji.off')
    print ("--------------------------------------------------------------------------")
    print("Device must not be connected and powered on at boot")
    print("Please plug in your DJI device and power it on")
    raw_input('Press Enter when complete')
    print("Waiting for device to initilize....")
    print ("--------------------------------------------------------------------------")
    time.sleep(10)
    os.system('ls /dev/tty* | sed -e "s#.*/##g" > /tmp/dji.on')
    os.system('diff /tmp/dji.on /tmp/dji.off | grep "<" | sed -e "s/.* //" > /tmp/dji.port')
    os.remove("/tmp/dji.on")
    os.remove("/tmp/dji.off")
    port = open('/tmp/dji.port').read()
    port = port.replace('\n', '')
    os.remove("/tmp/dji.port")
    if not port:
        print ("No DJI product was detected. Please unplug it, rerun the script and follow the instructions")
        sys.exit()
    else:
        print ("Found a DJI gizmo at: /dev/{}".format(port))

    return

def configure_usb():
    #serial.tools.list_ports

    # Serial Port should resemble: '/dev/cu.usbmodem1425'
    global ser
    ser = serial.Serial("/dev/" + port)
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
        print ("dji_system.bin delivered via FTP")
        ftp.cwd('upgrade')
        if '.bin' in ftp.nlst() :
            print (".bin already exists...")
        else :
            ftp.mkd("/upgrade/.bin")
        fh.close()
        ftp.quit()

        
    return 

def generate_update_packets(device):
    
    global packet_1 
    global packet_2 
    global packet_3 
    global packet_4

    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/dji_system.bin"
    # Pack file size into 4 byte Long little endian
    file_size = struct.pack('<L',int(os.path.getsize(dir_path)))

    if device == 1: #Aircraft
        # Enter upgrade mode (delete old file if exists)
        packet_1 = bytearray.fromhex(u'55 16 04 FC 2A 28 65 57 40 00 07 00 00 00 00 00 00 00 00 00 27 D3')
        # Enable Reporting
        packet_2 = bytearray.fromhex(u'55 0E 04 66 2A 28 68 57 40 00 0C 00 88 20')

        # 551A04B12A286B5740000800YYYYYYYY0000000000000204XXXX
        #YYYYYYYY - file size in little endian
        #XXXX - CRC as produced by table_crc.py

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
    
    elif device == 2: #RC
        # Enter upgrade mode (delete old file if exists)
        packet_1 = bytearray.fromhex(u'55 16 04 FC 2A 2D E7 27 40 00 07 00 00 00 00 00 00 00 00 00 9F 44')
        # Enable Reporting
        packet_2 = bytearray.fromhex(u'55 0E 04 66 2A 2D EA 27 40 00 0C 00 2C C8')

        packet_3 = bytearray.fromhex(u'55 1A 04 B1 2A 2D EC 27 40 00 08 00')
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
        packet_4 = bytearray.fromhex(u'55 1E 04 8A 2A 2D 02 28 40 00 0A 00')
        packet_4 += md5_check

        packet_length = len(packet_4)
        crc = calc_checksum(packet_4,packet_length)
        crc = struct.pack('<H',crc)
        packet_4 += crc

    elif device == 3: #Goggles
        # Enter upgrade mode (delete old file if exists)
        packet_1 = bytearray.fromhex(u'55 16 04 FC 2A 3C F7 35 40 00 07 00 00 00 00 00 00 00 00 00 0C 29')
        # Enable Reporting
        packet_2 = bytearray.fromhex(u'55 0E 04 66 2A 3C FA 35 40 00 0C 00 48 02')

        packet_3 = bytearray.fromhex(u'55 1A 04 B1 2A 3C FD 35 40 00 08 00')
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
        packet_4 = bytearray.fromhex(u'55 1E 04 8A 2A 3C 5B 36 40 00 0A 00')
        packet_4 += md5_check

        packet_length = len(packet_4)
        crc = calc_checksum(packet_4,packet_length)
        crc = struct.pack('<H',crc)
        packet_4 += crc        

    else:
        print ("You picked an option not yet supported")

    return


if __name__ == "__main__":
    main()
