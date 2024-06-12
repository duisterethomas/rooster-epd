from epd_2in9_b import EPD_2in9_B

from machine import Pin
import select
import sys


# Set up the poll object
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# Init EPD and led pin
epd = EPD_2in9_B()
led = Pin(25, Pin.OUT)


while True:
    # Wait for input on stdin
    poll_results = poll_obj.poll()
    if poll_results:
        # Read the data from stdin (read data coming from PC)
        data = sys.stdin.readline().strip()
        # data[0] = colour
        # data[1:4] = text X position
        # data[4:7] = text Y position
        # data[7:] = text
        
        if len(data) > 4:
            # Get the colour
            if data[4] == "r":
                colour = "Red"
                imagered_colour = 0x00
                imageblack_colour = 0x00
            elif data[4] == "b":
                colour = "Black"
                imagered_colour = 0xff
                imageblack_colour = 0xff
            elif data[4] == "w":
                colour = "White"
                imagered_colour = 0xff
                imageblack_colour = 0x00
        
        if data == "init":
            print('Initializing display...')
            # Turn the display on
            led.on()
            
            # Clear the display
            epd.Clear(0xff, 0xff)
            
            # Init the layers
            epd.imageblack.fill(0x00)
            epd.imagered.fill(0xff)
        
        # Draw a line command
        elif data[0:4] == "line":
            if len(data) == 17:
                # Draw the line
                print(f'{colour} line X{int(data[5:8])} Y{int(data[8:11])} W{int(data[11:14])} H{int(data[14:17])}')
                epd.imagered.line(int(data[5:8]),
                                    int(data[8:11]),
                                    int(data[11:14]),
                                    int(data[14:17]),
                                    imagered_colour)
                epd.imageblack.line(int(data[5:8]),
                                    int(data[8:11]),
                                    int(data[11:14]),
                                    int(data[14:17]),
                                    imageblack_colour)
            else:
                print("Invalid parameters")
            
        # Draw a rectangle command
        elif data[0:4] == "rect":
            if len(data) == 18:
                # Draw the rectangle
                print(f'{colour}{" filled" * int(data[17])} rectangle X{int(data[5:8])} Y{int(data[8:11])} W{int(data[11:14])} H{int(data[14:17])}')
                epd.imagered.rect(int(data[5:8]),
                                int(data[8:11]),
                                int(data[11:14]),
                                int(data[14:17]),
                                imagered_colour, int(data[17]))
                epd.imageblack.rect(int(data[5:8]),
                                    int(data[8:11]),
                                    int(data[11:14]),
                                    int(data[14:17]),
                                    imageblack_colour, int(data[17]))
            else:
                print("Invalid parameters")
        
        # Draw text command
        elif data[0:4] == "text":
            if len(data) > 11:
                # Draw the text
                print(f'{colour} text X{int(data[5:8])} Y{int(data[8:11])}: {data[11:]}')
                epd.imagered.text(data[11:], int(data[5:8]), int(data[8:11]), imagered_colour)
                epd.imageblack.text(data[11:], int(data[5:8]), int(data[8:11]), imageblack_colour)
            else:
                print("Invalid parameters")
        
        # Show the result command
        elif data == "show":
            print("Showing final result...")
            # Display it
            epd.display()
            
            # Turn led off
            led.off()
        
        # Exit/cancel command
        elif data == "exit":
            print("Exit")
            # Turn led off
            led.off()
        
        # Unknown command recieved
        else:
            print(f"Unknown command: {data}")