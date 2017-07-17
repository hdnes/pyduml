#!/usr/bin/python

# HDnes pythonDUML
# Thanks Hostile for the fireworks grepping all the fish.
# Thanks the_lord for the sniffing
# Thanks hfman & jaydee for the usb and ftp work
# root/flash selection and auto downloader added by vk2fro

import time
import os
import sys
import shutil
import serial
import usb.core
import usb.util
import struct
import hashlib
from table_crc import *

global type
global firmware
global device
if os.path.exists('./dji_system.bin')==True:
    print ("removing stale dji_system.bin")
    os.remove("dji_system.bin")

print ("--------------------------------------------------------------------------")
device = input('Select device number as follows: Aircraft = [1], RC = [2], Goggles = [3] : ')
print ("--------------------------------------------------------------------------")
type = input('Please choose a operation to execute on your device: Flash [1] Root [2] : ')
print ("--------------------------------------------------------------------------")
if type==1 and device==1:
    print ("--------------------------------------------------------------------------")
    firmware = input('Select a firmware to flash: [1] 400 [2] 700 [3] 800 [4] 900: ')
    print ("--------------------------------------------------------------------------")
if device==1 and firmware==1:
    if os.path.exists('./V01.03.0400_Mavic_dji_system.bin')==False:
        print ("Downloading Firmware file .400 - this may take a bit - its ~100MB")
        os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0400_Mavic_dji_system.bin')
        shutil.copyfile ('V01.03.0400_Mavic_dji_system.bin', 'dji_system.bin')
    else:
        shutil.copyfile ('V01.03.0400_Mavic_dji_system.bin', 'dji_system.bin')
elif device==1 and firmware==2:
    if os.path.exists('./V01.03.0700_Mavic_dji_system.bin')==False:
        print ("Downloading Firmware file .700 - this may take a bit - its ~100MB")
        os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0700_Mavic_dji_system.bin')
        shutil.copyfile ('V01.03.0700_Mavic_dji_system.bin', 'dji_system.bin')
    else:
        shutil.copyfile ('V01.03.0700_Mavic_dji_system.bin', 'dji_system.bin')
elif device==1 and firmware==3:
    if os.path.exists('./V01.03.0800_Mavic_dji_system.bin')==False:
        print ("Downloading Firmware file .800 - this may take a bit - its ~100MB")
        os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0800_Mavic_dji_system.bin')
        shutil.copyfile ('V01.03.0800_Mavic_dji_system.bin', 'dji_system.bin')
    else:
        shutil.copyfile ('V01.03.0800_Mavic_dji_system.bin', 'dji_system.bin')
elif device==1 and firmware==4:
    if os.path.exists('./V01.03.0900_Mavic_dji_system.bin')==False:
        print ("Downloading Firmware file .900 - this may take a bit - its ~100MB")
        os.system ('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0900_Mavic_dji_system.bin')
        shutil.copyfile ('V01.03.0900_Mavic_dji_system.bin', 'dji_system.bin')
    else:
        shutil.copyfile ('V01.03.0900_Mavic_dji_system.bin', 'dji_system.bin')
if type==1 and device==2:
    print ("--------------------------------------------------------------------------")
    firmware = input('Select a firmware to flash: [1] 400 [2] 700 : ')
    print ("--------------------------------------------------------------------------")
if device==2 and firmware==1:
    if os.path.exists('./V01.03.0400_RC_Mavic_dji_system.bin')==False:
        print ("Downloading the RC .400 firmware - please be patient")
        os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0400_RC_Mavic_dji_system.bin')
        shutil.copyfile ('V01.03.0400_RC_Mavic_dji_system.bin', 'dji_system.bin')
    else:
        shutil.copyfile ('V01.03.0400_RC_Mavic_dji_system.bin', 'dji_system.bin')
elif device==2 and firmware==2:
    if os.path.exists('./V01.03.0700_RC_Mavic_dji_system.bin')==False:
        print ("Downloading the RC .700 firmware - please be patient")
        os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0700_RC_Mavic_dji_system.bin')
        shutil.copyfile ('V01.03.0700_RC_Mavic_dji_system.bin', 'dji_system.bin')
    else:
        shutil.copyfile ('V01.03.0700_RC_Mavic_dji_system.bin', 'dji_system.bin')
if type==1 and device==3:
    print ("--------------------------------------------------------------------------")
    firmware = input ("Select a firmware to flash [1] 700 [2] 800 :")
    print ("--------------------------------------------------------------------------")
if device==3 and firmware==1:
    if os.path.exists('./V01.03.0700_Goggles_dji_system.bin')==False:
        print ("downloading Goggles 700 firmware file. Please wait...")
        os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0700_Goggles_dji_system.bin')
        shutil.copyfile ('V01.03.0700_Goggles_dji_system.bin', 'dji_system.bin')
    else:
        shutil.copyfile ('V01.03.0700_Goggles_dji_system.bin', 'dji_system.bin')

elif device==3 and firmware==2:
    if os.path.exists('./V01.03.0800_Goggles_dji_system.bin')==False:
        print ("downloading Goggles 800 firmware file. Please wait...")
        os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0800_Goggles_dji_system.bin')
        shutil.copyfile ('V01.03.0800_Goggles_dji_system.bin', 'dji_system.bin')
    else:
        shutil.copyfile ('V01.03.0800_Goggles_dji_system.bin', 'dji_system.bin')

if type==2:
    shutil.copyfile('fireworks.tar', 'dji_system.bin')
        
if device==1:
    print ("Running Exploit for Aircraft")
elif device ==2:
    print ("Running Exploit for RC")
    print ("----------------------")
    print ("Rooting RC is finicky, if having difficulties try the following")
    print ("--------------------------------------------------------------------------")
    print ("after root completes:")
    print ("1: unplug before turning off")
    print ("2: turn off")
    print ("3: turn on (without usb connected)")
    print ("4: turn off")
    print ("5: plug in usb and turn on")

elif device == 3:
    print ("Running Exploit for Goggles")

print ("--------------------------------------------------------------------------")    

def main():
   
    #probe_for_device()
    configure_usb()
    generate_update_packets()
    write_packet(packet_1) # Enter upgrade mode (delete old file if exists) 
    write_packet(packet_2) # Enable Reporting
    upload_binary()
    write_packet(packet_3) # Send File size
    write_packet(packet_4) # Send MD5 Hash for verification and Start Upgrade
    print ("--------------------------------------------------------------------------") 
    print ("Upgrade/Downgrade in Progress - May take a while....")
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

    # Serial Port should resemble: '/dev/cu.usbmodem1425'
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
        print ("dji_system.bin delivered via FTP")
        ftp.cwd('upgrade')
        if '.bin' in ftp.nlst() :
            print '.bin already exists...'
        else :
            ftp.mkd("/upgrade/.bin")
        fh.close()
        ftp.quit()

        
    return 

def generate_update_packets():
    
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

    elif device == 3 and firmware ==2 or type==2: #Goggles
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
