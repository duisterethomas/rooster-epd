from time import sleep

from PySide6.QtCore import QObject, Signal

class Worker(QObject):
    finished = Signal()
    
    def __init__(self, pico, command):
        super(Worker, self).__init__()
        self.pico = pico
        self.command = command
    
    # Worker to send commands to the pico
    def run(self):
        self.pico.write(f"{self.command}\r".encode())
        
        recieved = self.pico.read_until().strip().decode()
        while recieved != "done":
            if recieved:
                print(recieved)
            
            sleep(0.1)
            recieved = self.pico.read_until().strip().decode()
        
        self.finished.emit()