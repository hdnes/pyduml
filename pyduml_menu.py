#!/usr/bin/python
import shutil

# root/flash selection and auto downloader added by vk2fro
def pyduml_UI():

    global hack
    global type
    global firmware



    hack = 0
    type = 0
    firmware = 0
    device = 0

    print ("--------------------------------------------------------------------------")
    device = input('Select device number as follows: Aircraft = [1], RC = [2], Goggles = [3] : ')
    print ("--------------------------------------------------------------------------")
    type = input('Please choose a operation to execute on your device: Flash [1] Root [2] : ')
    print ("--------------------------------------------------------------------------")
    if type==1 and device==1:
        print ("------------------------------------------------------------------------------")
        print ("Choose a firmware - version 400 and 700 have pre rooted options for mavic only")
        firmware = input('Select a firmware to flash: [1] 400 [2] 700 [3] 800 [4] 900: ')
        print ("------------------------------------------------------------------------------")
    if device==1 and firmware==1:
        print ("------------------------------------------------------------------------------")
        hack = input ('Would you like a pre-rooted firmware? [1] NO! [2] Yes please! :')
        print ("------------------------------------------------------------------------------")
    if device==1 and firmware==2:
        print ("------------------------------------------------------------------------------")
        hack = input ('Would you like a pre-rooted firmware? [1] NO! [2] Yes please! :')
        print ("------------------------------------------------------------------------------")
    if device==1 and firmware==1 and hack==1:
        if os.path.exists('./V01.03.0400_Mavic_dji_system.bin')==False:
            print ("Downloading Firmware file .400 - this may take a bit - its ~100MB")
            os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0400_Mavic_dji_system.bin')
            shutil.copyfile ('V01.03.0400_Mavic_dji_system.bin', 'dji_system.bin')
        else:
            shutil.copyfile ('V01.03.0400_Mavic_dji_system.bin', 'dji_system.bin')
    elif device==1 and firmware==2 and hack==1:
        if os.path.exists('./V01.03.0700_Mavic_dji_system.bin')==False:
            print ("Downloading Firmware file .700 - this may take a bit - its ~100MB")
            os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0700_Mavic_dji_system.bin')
            shutil.copyfile ('V01.03.0700_Mavic_dji_system.bin', 'dji_system.bin')
        else:
            shutil.copyfile ('V01.03.0700_Mavic_dji_system.bin', 'dji_system.bin')
    elif device==1 and firmware==3 and hack==1:
        if os.path.exists('./V01.03.0800_Mavic_dji_system.bin')==False:
            print ("Downloading Firmware file .800 - this may take a bit - its ~100MB")
            os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/V01.03.0800_Mavic_dji_system.bin')
            shutil.copyfile ('V01.03.0800_Mavic_dji_system.bin', 'dji_system.bin')
        else:
            shutil.copyfile ('V01.03.0800_Mavic_dji_system.bin', 'dji_system.bin')
    elif device==1 and firmware==4 and hack==1:
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
            
    if device==1 and firmware==1 and hack==2:
        if os.path.exists('./mavic_combined_400_root.bin')==False:
            print ('Downloading pre-rooted .400 firmware for Mavic Aircraft. This may take a bit, its ~100MB')
            os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/mavic_combined_400_root.bin')
            shutil.copyfile ('mavic_combined_400_root.bin', 'dji_system.bin')
        else:
            shutil.copyfile ('mavic_combined_400_root.bin', 'dji_system.bin')
            
    elif device==1 and firmware==2 and hack==2:
        if os.path.exists('./mavic_combined_700_root.bin')==False:
            print ('Downloading pre-rooted .700 firmware for Mavic Aircraft. This may take a bit, its ~100MB')
            os.system('wget https://github.com/MAVProxyUser/dji_system.bin/raw/master/mavic_combined_700_root.bin')
            shutil.copyfile ('mavic_combined_700_root.bin', 'dji_system.bin')
        else:
            shutil.copyfile ('mavic_combined_700_root.bin', 'dji_system.bin')

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

    return device;
