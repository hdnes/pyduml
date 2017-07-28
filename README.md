Pyduml
------
Python based DUML [DJI Universal Markup Language] Exploit & FW upgrade/downgrade tool.

Thanks to the following:
@POV @hostile, @the_lord, @hfman, @jayemdee

----------------------------------------------------------------
Dependencies:

- python 2.7 (not sure if 3+ has been tested yet)

- pyserial 3.3 package (install with 'pip install pyserial' and then follow that with 'pip install --upgrade pyserial' to be sure you are on newest version)

- pathlib 1.0.1 (install with 'pip install pathlib')

----------------------------------------------------------------
Normal Usage: python pyduml.py
This will autodetect your device and communications port and setup the RNDIS network for ftp file transfer under linux.  
If something doesnt work right with this you can use the advanced usage instructions below. 

----------------------------------------------------------------
Advanced Usage: python pyduml.py serial_port debugmode(optional)

Serial Port should resemble '/dev/cu.usbmodemXXXX' on Apple 
or on Linux should be something like '/dev/ttyACM0'where XXXX 
is your specific device number connected

----------------------------------------------------------------

Use included RedHerring fireworks.tar to obtain root (DUMLHerring aka Dumb Herring).  Just rename it to dji_system.bin.
Run in standalone mode for use as a firmware upgrade / downgrade tool firmware bins here: [dji_system.bin](https://github.com/MAVProxyUser/dji_system.bin)


![HDnes](http://piq.codeus.net/static/media/userpics/piq_291737_400x400.png)

![Mutated Herrings have hit the seas...](https://raw.githubusercontent.com/hdnes/pyduml/master/history.jpg)

### #DeejayeyeHackingClub information repos aka "The OG's" (Original Gangsters)

http://dji.retroroms.info/ - "Wiki"

https://github.com/fvantienen/dji_rev - This repository contains tools for reverse engineering DJI product firmware images.

https://github.com/Bin4ry/deejayeye-modder - APK "tweaks" for settings & "mods" for additional / altered functionality

https://github.com/hdnes/pyduml - Assistant-less firmware pushes and DUMLHacks referred to as DUMBHerring when used with "fireworks.tar" from RedHerring. DJI silently changes Assistant? great... we will just stop using it.

https://github.com/MAVProxyUser/P0VsRedHerring - RedHerring, aka "July 4th Independence Day exploit", "FTPD directory transversal 0day", etc. (Requires Assistant). We all needed a public root exploit... why not burn some 0day?

https://github.com/MAVProxyUser/dji_system.bin - Current Archive of dji_system.bin files that compose firmware updates referenced by MD5 sum. These can be used to upgrade and downgrade, and root your I2, P4, Mavic, Spark, Goggles, and Mavic RC to your hearts content. (Use with pyduml or DUMLDore)

https://github.com/MAVProxyUser/firm_cache - Extracted contents of dji_system.bin, in the future will be used to mix and match pieces of firmware for custom upgrade files. This repo was previously private... it is now open.

https://github.com/MAVProxyUser/DUMLrub - Ruby port of PyDUML, and firmware cherry picking tool. Allows rolling of custom firmware images.

https://github.com/jezzab/DUMLdore - Even windows users need some love, so DUMLDore was created to help archive, and flash dji_system.bin files on windows platforms.

https://github.com/MAVProxyUser/DJI_ftpd_aes_unscramble - DJI has modified the GPL Busybox ftpd on Mavic, Spark, & Inspire 2 to include AES scrambling of downloaded files... this tool will reverse the scrambling
