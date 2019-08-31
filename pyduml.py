#!/usr/bin/python

# HDnes pythonDUML
# Thanks Hostile for the fireworks grepping all the fish.
# Thanks the_lord for the sniffing
# Thanks hfman & jayemdee for the usb and ftp work
# Ugly SparkRC stuff from jan2642,bin4ry and the_lord

import time
import os
import platform
import sys
import serial
import struct
import hashlib
import socket

from table_crc import *
from utils import *
from pathlib import Path
from ftplib import FTP
from serial.tools import list_ports

def main():
    platform_detection() 
    device_selection_prompt()
    if device != 4:
        configure_usbserial()
        check_network()
    elif device == 4:
        configure_socket()
    define_firmware()
    if device != 4:
        generate_update_packets()
        write_packet(packet_1) # Enter upgrade mode (delete old file if exists) 
        write_packet(packet_2) # Enable Reporting
        upload_binary()
        write_packet(packet_3) # Send File size
        write_packet(packet_4) # Send MD5 Hash for verification and Start Upgrade
    elif device == 4:
        doSparkRc()
    print ("--------------------------------------------------------------------------") 
    print ("If you are upgrading/downgrading firmware, this may take a while.\nIf you are rooting, the process is almost instant. wait a few seconds and reboot your device.")
    if device != 4:
        ser.close
    elif device == 4:
        s.close()
    return

def platform_detection():
    global sysOS
    sysOS = platform.system()
    print("\033c") # clear screen
    return sysOS

def device_selection_prompt():
	global device
	device = int(input('\nSelect device number as follows: Aircraft = [1], RC = [2], Goggles = [3], SparkRC = [4]: '))
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

	elif device == 4:
		print("Spark RC selected")
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

def configure_socket():
	global s
	TCP_IP = '192.168.1.1'
	TCP_PORT = 19003
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))

def write_packet(data):
    ser.write(data)     # write a string
    time.sleep(0.1)
    hexout = ' '.join(format(x, '02X') for x in data)
    if len(sys.argv) > 2 and sys.argv[2] == "debugmode":
        print (hexout)
    else:
        print("Sent DUML packet...\n")
    return

def send_duml_tcp(socket, source, target, cmd_type, cmd_set, cmd_id, payload = None):
    global sequence_number
    sequence_number = 0x34eb
    packet = bytearray.fromhex(u'55')
    length = 13
    if payload is not None:
        length = length + len(payload)

    if length > 0x3ff:
        print("Packet too large")
        exit(1)

    packet += struct.pack('B', length & 0xff)
    packet += struct.pack('B', (length >> 8) | 0x4) # MSB of length and protocol version
    hdr_crc = calc_pkt55_hdr_checksum(0x77, packet, 3)
    packet += struct.pack('B', hdr_crc)
    packet += struct.pack('B', source)
    packet += struct.pack('B', target)
    packet += struct.pack('<H', sequence_number)
    packet += struct.pack('B', cmd_type)
    packet += struct.pack('B', cmd_set)
    packet += struct.pack('B', cmd_id)

    if payload is not None:
        packet += payload

    crc = calc_checksum(packet, len(packet))
    packet += struct.pack('<H',crc)
    socket.send(packet)
    if len(sys.argv) > 2 and sys.argv[2] == "debugmode":
        print(' '.join(format(x, '02x') for x in packet))
    else:
        print("Sent DUML packet...\n")

    sequence_number += 1

def define_firmware():
    global firmware_file
    if device != 4:
        firmware_file = Path("dji_system.bin").absolute()
    elif device == 4:
        firmware_file = Path("fw.tar").absolute()
    if firmware_file.is_file() is False:
        sys.exit("Error: No dji_system.bin or fw.tar found in CWD or it is not a valid file.\n")
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

def doSparkRc():
    f = open (str(firmware_file), "rb")
    data = f.read()
    f.close()
    
    send_duml_tcp(s, 0x02, 0x1b, 0x40, 0x00, 0x07, bytearray.fromhex(u'00 00 00 00 00 00 00 00 00'))

    packet_08 = bytearray.fromhex(u'00')
    packet_08 += struct.pack('<I', len(data))
    packet_08 += bytearray.fromhex(u'00 00 00 00 00 00 01 04')
    send_duml_tcp(s, 0x02, 0x1b, 0x40, 0x00, 0x08, packet_08)

    for i in range(0, int(len(data)//1000)):
        packet_09 = bytearray.fromhex(u'00')
        packet_09 += struct.pack('<I', i)
        packet_09 += struct.pack('<H', 1000)
        packet_09 += data[i * 1000:(i + 1) * 1000]
        send_duml_tcp(s, 0x02, 0x1b, 0x00, 0x00, 0x09, packet_09)

    i += 1
    remain = len(data) % 1000
    packet_09 = bytearray.fromhex(u'00')
    packet_09 += struct.pack('<I', i)
    packet_09 += struct.pack('<H', remain)
    packet_09 += data[i * 1000:]
    send_duml_tcp(s, 0x02, 0x1b, 0x00, 0x00, 0x09, packet_09)

    filehash = hashlib.md5()
    filehash.update(data)
    filehash = filehash.digest()
    packet_0a = bytearray.fromhex(u'00')
    packet_0a += filehash
    send_duml_tcp(s, 0x02, 0x1b, 0x40, 0x00, 0x0a, packet_0a)

# from comm_serial2pcap.py
# https://github.com/mefistotelis/phantom-firmware-tools/issues/25#issuecomment-306052129
def calc_pkt55_hdr_checksum(seed, packet, plength):
    arr_2A103 = [0x00,0x5E,0xBC,0xE2,0x61,0x3F,0xDD,0x83,0xC2,0x9C,0x7E,0x20,0xA3,0xFD,0x1F,0x41,
        0x9D,0xC3,0x21,0x7F,0xFC,0xA2,0x40,0x1E,0x5F,0x01,0xE3,0xBD,0x3E,0x60,0x82,0xDC,
        0x23,0x7D,0x9F,0xC1,0x42,0x1C,0xFE,0xA0,0xE1,0xBF,0x5D,0x03,0x80,0xDE,0x3C,0x62,
        0xBE,0xE0,0x02,0x5C,0xDF,0x81,0x63,0x3D,0x7C,0x22,0xC0,0x9E,0x1D,0x43,0xA1,0xFF,
        0x46,0x18,0xFA,0xA4,0x27,0x79,0x9B,0xC5,0x84,0xDA,0x38,0x66,0xE5,0xBB,0x59,0x07,
        0xDB,0x85,0x67,0x39,0xBA,0xE4,0x06,0x58,0x19,0x47,0xA5,0xFB,0x78,0x26,0xC4,0x9A,
        0x65,0x3B,0xD9,0x87,0x04,0x5A,0xB8,0xE6,0xA7,0xF9,0x1B,0x45,0xC6,0x98,0x7A,0x24,
        0xF8,0xA6,0x44,0x1A,0x99,0xC7,0x25,0x7B,0x3A,0x64,0x86,0xD8,0x5B,0x05,0xE7,0xB9,
        0x8C,0xD2,0x30,0x6E,0xED,0xB3,0x51,0x0F,0x4E,0x10,0xF2,0xAC,0x2F,0x71,0x93,0xCD,
        0x11,0x4F,0xAD,0xF3,0x70,0x2E,0xCC,0x92,0xD3,0x8D,0x6F,0x31,0xB2,0xEC,0x0E,0x50,
        0xAF,0xF1,0x13,0x4D,0xCE,0x90,0x72,0x2C,0x6D,0x33,0xD1,0x8F,0x0C,0x52,0xB0,0xEE,
        0x32,0x6C,0x8E,0xD0,0x53,0x0D,0xEF,0xB1,0xF0,0xAE,0x4C,0x12,0x91,0xCF,0x2D,0x73,
        0xCA,0x94,0x76,0x28,0xAB,0xF5,0x17,0x49,0x08,0x56,0xB4,0xEA,0x69,0x37,0xD5,0x8B,
        0x57,0x09,0xEB,0xB5,0x36,0x68,0x8A,0xD4,0x95,0xCB,0x29,0x77,0xF4,0xAA,0x48,0x16,
        0xE9,0xB7,0x55,0x0B,0x88,0xD6,0x34,0x6A,0x2B,0x75,0x97,0xC9,0x4A,0x14,0xF6,0xA8,
        0x74,0x2A,0xC8,0x96,0x15,0x4B,0xA9,0xF7,0xB6,0xE8,0x0A,0x54,0xD7,0x89,0x6B,0x35]

    chksum = seed
    for i in range(0, plength):
        chksum = arr_2A103[((packet[i] ^ chksum) & 0xFF)];
    return chksum	
	
if __name__ == "__main__":
    main()
