from kivy.uix.popup import Popup
import time
import serial

# 시리얼 통신을 위한 포트 번호와 전송 속도를 설정합니다.
port = "COM5"  # 포트 번호
baudrate = 9600  # 전송 속도를 설정합니다.

# 시리얼 통신을 위한 객체를 생성합니다.
ser = serial.Serial("COM5", baudrate)
class shelves:
    def __init__(self, location_list):
        self.location_list = location_list

    def rotate(self):
        for location in self.location_list:
            # Put some code to rotate the shelf
            print("rotating to . . .", location)
            time.sleep(3)
            ser.write(str(location).encode())
            while True:
                if ser.in_waiting > 0:
                    my_variable = int(ser.readline().decode().rstrip())
                    print("Received variable:", my_variable)
                    break
