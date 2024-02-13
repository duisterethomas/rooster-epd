from os.path import exists
from time import sleep
import serial
import glob
import sys

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# Connect the pico
available_ports = serial_ports()
print('Available ports:')
for available_port in enumerate(available_ports):
    print(f"{available_port[0]}. {available_port[1]}")
port = available_ports[int(input("Port: "))]

pico = serial.Serial(port=port, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
pico.flush()

data = ""

while data not in ("exit", "cancel"):
    data = input("Data to send: ")

    if data != "exit":
        pico.write(f"{data}\r".encode())
        recieved = pico.read_until().strip()
        while not recieved:
            sleep(0.1)
            recieved = pico.read_until().strip()
        print(recieved.decode())