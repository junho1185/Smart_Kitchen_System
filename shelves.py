from kivy.uix.popup import Popup
import time
import serial

# 시리얼 통신을 위한 포트 번호와 전송 속도를 설정합니다.
port = "COM3"  # 포트 번호
baudrate = 9600  # 전송 속도를 설정합니다.

# 시리얼 통신을 위한 객체를 생성합니다.
ser = serial.Serial("COM3", baudrate)
class shelves:
    def __init__(self, location_list):
        self.location_list = location_list

    def rotate(self):
        for location in self.location_list:
            # Put some code to rotate the shelf
            print("rotating to . . .", location)
            ser.write(location)
            # time.sleep(3)