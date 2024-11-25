from json import load, dump, loads, dumps
from select import poll, POLLIN
from os import remove, listdir
import sys

from machine import Pin, mem32

# Set led pin
led = Pin('LED', Pin.OUT)

# Turn on led
led.on()

# Load the save file
if "save.json" in listdir("."):
    with open('save.json', 'r') as file:
        save = load(file)
else:
    save = None

# Check if connected to pc
SIE_STATUS = const(0x50110000+0x50)
CONNECTED = const(1<<16)
SUSPENDED = const(1<<4)
if (mem32[SIE_STATUS] & (CONNECTED | SUSPENDED)) == CONNECTED:
    led.off()
    
    # Set up the poll object
    poll_obj = poll()
    poll_obj.register(sys.stdin, POLLIN)
    
    while True:
        # Wait for input on stdin
        poll_results = poll_obj.poll()
        if poll_results:
            # Read the data from stdin (read data coming from PC)
            data = sys.stdin.readline().strip()
            
            # Ping command
            if data == 'ping':
                print('rooster_epd')
            
            # Version check command
            elif data == 'vchk':
                # Return the version if it exists, otherwise return VX.X.X
                if "version.txt" in listdir("."):
                    with open('version.txt', 'r') as file:
                        for line in file:
                            print(line)
                else:
                    print("VX.X.X")
                
                print('done')
            
            # List current files command
            elif data == 'list':
                for file in listdir('.'):
                    print(file)
                
                print('done')
            
            # Upload start command
            elif data[:4] == 'upls':
                filename = data[5:]
                
                file = open(filename, 'w')
                
                firstline = True
                # Wait until upload end command
                while data != 'uple':
                    # Wait for input on stdin
                    poll_results = poll_obj.poll()
                    if poll_results:
                        # Read the data from stdin (read data coming from PC)
                        data = sys.stdin.readline().strip()
                        
                        # Write the data to the file if not upload end command
                        if data != 'uple':
                            # Write new line if not first line
                            if not firstline:
                                file.write('\n')
                            else:
                                firstline = False
                                
                            # Write the actual line
                            file.write(data[1:])
                
                # Save and close the file
                file.close()
                
                print('done')
            
            # Delete file command
            elif data[:4] == 'fdel':
                remove(data[5:])
                
                print('done')
            
            # Load data command
            elif data == 'load':
                if save != None:
                    print(dumps(save))
                    
                    print('done')
                else:
                    print('fail')
                    
                    print('done')
            
            # Dump data command
            elif data[:4] == 'dump':
                save = loads(data[5:])
                
                with open('save.json', 'w') as file:
                    dump(save, file)
                
                print('done')
            
            # Let screen_updating handle the command
            else:
                from screen_updating import handle_command
                
                handle_command(data)

# Else run normal code
else:
    from screen_updating import connect, sync
    
    # Connect wlan
    connect(60)
    
    # Sync with zermelo
    sync()