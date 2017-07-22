#!/usr/bin/python

# HDnes pythonDUML
# Thanks Hostile for the fireworks grepping all the fish.
# Thanks the_lord for the sniffing
# Thanks hfman & jayemdee for the usb and ftp work

import time
import os
import platform
import sys
import serial
import struct
import hashlib

from table_crc import *
from utils import *
from pathlib import Path
from ftplib import FTP
from serial.tools import list_ports

def main():
    platform_detection()
    configure_usbserial()
    check_network()    
    device_selection_prompt()
    define_firmware()
    generate_update_packets()
    write_packet(packet_1) # Enter upgrade mode (delete old file if exists) 
    write_packet(packet_2) # Enable Reporting
    upload_binary()
    write_packet(packet_3) # Send File size
    write_packet(packet_4) # Send MD5 Hash for verification and Start Upgrade
    print ("--------------------------------------------------------------------------") 
    print ("If you are upgrading/downgrading firmware, this may take a while.\nIf you are rooting, the process is almost instant. wait a few seconds and reboot your device.")
    ser.close
    return

def platform_detection():
    global sysOS
    sysOS = platform.system()
    print("\033c") # clear screen
    return sysOS

def device_selection_prompt():
	global device
	device = input('\nSelect device number as follows: Aircraft = [1], RC = [2], Goggles = [3] : ')
	if device == 1:
	    print ("Exploit for Aircraft selected")
	elif device == 2:
	    print ("Exploit for RC selected")
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
	    print ("Exploit for Goggles selected")

	print ("--------------------------------------------------------------------------")    
	return

def find_port():
    try:
        dji_dev = list(list_ports.grep("2ca3:001f"))[0][0]
        return dji_dev
    except:
        sys.exit("Error: No DJI device found plugged to your system. Please re-plug / reboot device and try again.\n")

def check_network():
    # Linux specific magic
    if sysOS == 'Linux':
        print("Attempting to to set IP on usb0...")
        set_ip_addr('usb0', '192.168.42.1')
        try:
            iface_exists("usb0")
            os.system('/sbin/ifconfig usb0 up') # linux specific hack: cant find a pure python way of bringing usb0 up after config
            print("Network setup successful.")
        except:
            sys.exit("Error: Unknown failure configuring RNDIS device.")
    return

def configure_usbserial():
    global comport

    # no command line args
    if len(sys.argv) < 2:
        comport = find_port()
        print ("Preparing to run pythonDUML exploit from a " + sysOS + " Machine using com port: " +comport)
        print ("If this is not the right device you can override by passing the device name as first argument to this script.\n")
    # parse command line args
    else:
        comport = sys.argv[1]
        print ("Preparing to run pythonDUML exploit from a " + sysOS + " Machine using com port: " +comport+ "\n")
    try:
        global ser
        ser = serial.Serial(comport)
        ser.baudrate = 115200
    except:
        print("Error: Could not open communications port " + comport + ".\n")
        sys.exit(0)
    return

def write_packet(data):
    ser.write(data)     # write a string
    time.sleep(0.1)
    hexout = ' '.join(format(x, '02X') for x in data)
    if len(sys.argv) > 2 and sys.argv[2] == "debugmode":
        print (hexout)
    else:
        print("Sent DUML packet...\n")
    return

def define_firmware():
    global firmware_file
    firmware_file = Path("dji_system.bin").absolute()
    if firmware_file.is_file() is False:
        sys.exit("Error: No dji_system.bin found in CWD or it is not a valid file.\n")
    return

def upload_binary():
    print("Opening FTP connection to 192.168.42.2...\n")
    ftp = FTP("192.168.42.2", "Gimme", "DatROot!")
    fh = open(str(firmware_file), 'rb')
    ftp.set_pasv(True)	# this is the fix for buggy ftp uploads we ran into in early days -jayemdee
    ftp.storbinary('STOR /upgrade/dji_system.bin', fh)
    print (str(firmware_file) + " uploaded to FTP with a remote file size of: " + str(ftp.size("/upgrade/dji_system.bin")))
    ftp.cwd('upgrade')
    if '.bin' in ftp.nlst() :
        print(".bin directory already exists. Skipping directory creation...\n")
    else :
        print("Creating /upgrade/.bin directory...\n")
        ftp.mkd("/upgrade/.bin")
    fh.close()
    ftp.quit()        
    return 

def generate_update_packets():
    
    global packet_1 
    global packet_2 
    global packet_3 
    global packet_4

    # Pack file size into 4 byte Long little endian
    dir_path = str(firmware_file)
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
        sys.exit("Invalid Selection. Exiting.\n")

    return

if __name__ == "__main__":
    main()
