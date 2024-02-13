import select
import sys
from machine import Pin, SPI
import framebuf
import utime
      
# Display resolution
EPD_WIDTH       = 152
EPD_HEIGHT      = 296

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

WF_PARTIAL_2IN66 =[
0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x40,0x40,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x0A,0x00,0x00,0x00,0x00,0x00,0x02,0x01,0x00,0x00,
0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x22,0x22,0x22,0x22,0x22,0x22,
0x00,0x00,0x00,0x22,0x17,0x41,0xB0,0x32,0x36,
]

class EPD_2in9_B:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.lut = WF_PARTIAL_2IN66
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000) # type: ignore
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        self.buffer_black = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        self.imageblack = framebuf.FrameBuffer(self.buffer_black, self.width, self.height, framebuf.MONO_HLSB)
        self.imagered = framebuf.FrameBuffer(self.buffer_red, self.width, self.height, framebuf.MONO_HLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)


    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)
        
    def SetWindow(self, x_start, y_start, x_end, y_end):
        self.send_command(0x44)
        self.send_data((x_start>>3) & 0x1f)
        self.send_data((x_end>>3) & 0x1f)
        
        self.send_command(0x45)
        self.send_data(y_start&0xff)
        self.send_data((y_start&0x100)>>8)
        self.send_data((y_end&0xff))
        self.send_data((y_end&0x100)>>8)
        
    def SetCursor(self, x_start, y_start):
        self.send_command(0x4E)
        self.send_data(x_start & 0x1f)
        
        self.send_command(0x4f)
        self.send_data(y_start&0xff)
        self.send_data((y_start&0x100)>>8)
        
    def ReadBusy(self):
        utime.sleep_ms(50)
        while(self.busy_pin.value() == 1):  # 0: idle, 1: busy
            utime.sleep_ms(10)
        utime.sleep_ms(50)
        
    def TurnOnDisplay(self):
        self.send_command(0x20)
        self.ReadBusy()
        
    def init(self):
        self.reset()
        self.ReadBusy()
        self.send_command(0x12)
        self.ReadBusy() #waiting for the electronic paper IC to release the idle signal

        self.send_command(0x11)
        self.send_data(0x03)

        self.SetWindow(0, 0, self.width-1, self.height-1)
        
        self.send_command(0x21) #resolution setting
        self.send_data (0x00)
        self.send_data (0x80)
        
        
        self.SetCursor(0,0)
        self.ReadBusy()
    
        
    def display(self):
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
            
        self.send_command(0x24)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(~self.buffer_black[i + j * wide])  
        
        self.send_command(0x26)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(~self.buffer_red[i + j * wide])  

        self.TurnOnDisplay()

    
    def Clear(self, colorblack, colorred):
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
            
        self.send_command(0x24)
        self.send_data1([colorblack] * high * wide)
        
        self.send_command(0x26)
        self.send_data1([~colorred] * high * wide)
                                
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0X10) # deep sleep
        self.send_data(0x01)


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