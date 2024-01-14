import serial
from time import sleep

pico = serial.Serial(port="COM5", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
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