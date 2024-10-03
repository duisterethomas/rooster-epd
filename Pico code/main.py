import select
import json
import sys

from machine import Pin, mem32

# Set led pin
led = Pin('LED', Pin.OUT)

# Turn on led
led.on()

# Load the save file
try:
    with open('save.json', 'r') as file:
        save = json.load(file)
except OSError:  # open failed
    save = None

# Check if connected to pc
SIE_STATUS = const(0x50110000+0x50)
CONNECTED = const(1<<16)
SUSPENDED = const(1<<4)
if (mem32[SIE_STATUS] & (CONNECTED | SUSPENDED)) == CONNECTED:
    led.off()
    
    # Set up the poll object
    poll_obj = select.poll()
    poll_obj.register(sys.stdin, select.POLLIN)
    
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
                with open('version.txt', 'r') as file:
                    for line in file:
                        print(line)
            
            # Update start command
            elif data[:4] == 'upds':
                filename = data[5:]
                
                file = open(filename, 'w')
                
                # Wait until update end command
                while data != 'upde':
                    # Wait for input on stdin
                    poll_results = poll_obj.poll()
                    if poll_results:
                        # Read the data from stdin (read data coming from PC)
                        data = sys.stdin.readline().strip()
                        
                        file.write(f'{data}\n')
            
            # Load data command
            elif data == 'load':
                if save != None:
                    print(json.dumps(save))
                    
                    print('done')
                else:
                    print('fail')
            
            # Dump data command
            elif data[:4] == 'dump':
                save = json.loads(data[5:])
                
                with open('save.json', 'w') as file:
                    json.dump(save, file)
                
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