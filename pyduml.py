#!/usr/bin/python
# HDnes pythonDUML
# Thanks the_lord for the sniffing
# Thanks jaydee for the usb and ftp work

import os
import sys
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
	probe_for_device()
	configure_usb()
	generate_update_packets()
	write_packet(packet_1) # Enter upgrade mode (delete old file if exists)
	write_packet(packet_2) # Enable Reporting
	upload_binary()
	write_packet(packet_3) # Send File size
	write_packet(packet_4) # Send MD5 Hash for verification and Start Upgrade

	print "Firmware Upload Complete"

	return;

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

		return;

def configure_usb()	
	cfg = dev.get_active_configuration()
	intf = cfg[(5,0)]
	usb.util.claim_interface(dev, intf)
	ep = intf[1]
	print("Endpoint Address: " + str(ep.bEndpointAddress))
	print("Turning on CDC Abstract Control Module")
	# dev.ctrl_transfer(reqType, bReq, wVal, wIndex, [])
	ret = dev.ctrl_transfer(0xa1,0x21,0x0000,0x0004,[])

	return;

def write_packet(data)	
	
	#Convert sting if required
	#data = [ int(''.join([data[i], data[i+1]]), base=16) for i in range(0, len(data), 2)]
	print('%d/%d written' %(ep.write(data), len(data)))

	return;

def upload_binary():
	print('Info: Connecting to FTP...\n')
	try:
		ftp = FTP('192.168.42.2', 'herring', 'fisher', 'none', 3)
		ftp.retrlines('LIST')
		dir = 'upgrade'
		#file = open('dji_system.bin', 'rb')
		if dir in ftp.nlst():
			print('Info: Upgrade folder exists. Uploading firmware...\n')
		#	ftp.storbinary('STOR upgrade/dji_system.bin', file)
		#	file.close()
			ftp.quit()
		else:
			print('Error: No "upgrade" folder on this ftp. Something is wrong. Exiting!\n')
			ftp.quit()
	except:
		print("Error: Failed FTP Connection to aircraft. Exiting...\n")
		sys.exit(2)

	return;	

def generate_update_packets():
	# Enter upgrade mode (delete old file if exists)
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

	#print ' '.join(format(x, '02X') for x in packet_1)
	#print ' '.join(format(x, '02X') for x in packet_2)
	#print ' '.join(format(x, '02X') for x in packet_3)
	#print ' '.join(format(x, '02X') for x in packet_4)

	return;



if __name__ == "__main__":
    main()
