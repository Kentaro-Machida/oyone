import serial

class communicator():
    def __init__(self,port="/dev/ttyACAM0",baudrate=9600,timeout=0.1):
        self.serial_communicator = serial.Serial(port, baudrate, timeout=timeout)
        
    def serial_wirte(self,x:str):
        self.serial_communicator.write(bytes(x,'utf-8'))
