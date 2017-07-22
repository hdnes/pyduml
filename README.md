Pyduml
------
Python based DUML [DJI Universal Markup Language] Exploit & FW upgrade/downgrade tool.

Thanks to the following:
@POV @hostile, @the_lord, @hfman, @jayemdee

----------------------------------------------------------------
Dependencies:

python 2.7 (not sure if 3+ has been tested yet)
pyserial 3.3 package (install with 'pip install pyserial' and then follow that with 'pip install --upgrade pyserial' to be sure you are on newest version)
pathlib 1.0.1 (install with 'pip install pathlib')

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

