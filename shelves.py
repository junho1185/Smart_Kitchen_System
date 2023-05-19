from kivy.uix.popup import Popup
class shelves:
    def __init__(self, location_list):
        self.location_list = location_list

    def rotate(self):
        for location in self.location_list:
            # Put some code to rotate the shelf
            print("rotating to . . .", location)