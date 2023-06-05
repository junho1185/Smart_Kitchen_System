import time
import serial
from kivy.clock import Clock
import threading
class shelves:
    def __init__(self, location_list):
        self.location_list = location_list
        self.port = "/dev/ttyACM0"  # Port Number for Arduino
        self.bRate = 9600  # Board Rate
        self.ser = serial.Serial(self.port, self.bRate)  # Serial Communication Variable

        self.rot_thread = threading.Thread(target=self.rotate)


    def rotate(self, *args):
        for location in self.location_list:
            # Put some code to rotate the shelf
            print("rotating to . . .", location)
            self.arduinoSignal(location)

    def arduinoSignal(self, location):
        time.sleep(2)
        print('sending signal to the Arduino Board. . .')
        self.ser.write(str(location).encode())
        while True:
            if self.ser.in_waiting > 0:
                my_variable = int(self.ser.readline().decode().rstrip())
                print("Received variable:", my_variable)
                break
