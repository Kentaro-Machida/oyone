import serial
import time

class communicator():
    def __init__(self,port="/dev/ttyACM0",baudrate=115200,timeout=0.1):
        self.serial_communicator = serial.Serial(port, baudrate, timeout=timeout)
        
    def serial_wirte(self,x:str,delay=0):
        time.sleep(delay)
        self.serial_communicator.write(bytes(x,'UTF-8'))

    def serial_read(self, until='\n')->str:
        return self.serial_communicator.read_until(until)
