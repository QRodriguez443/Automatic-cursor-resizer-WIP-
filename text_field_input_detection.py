import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor
import pyautogui
from AutoMove_shared_variables import v
from mouse_speed import main

v('mouse_over_field', False) # init the "variable"

# Creates an event area on the screen that detects if the mouse is within its bounds.

class RectangleGuide(QWidget):
    def __init__(self):
        super().__init__()
        '''These settings were tweaked to accurately encapsulate the inner bounds of the 
        text selection field specifically for the swtor launcher.'''

        # Get the screen resolution dynamically
        self.screen_width, self.screen_height = pyautogui.size()

        # Define the coordinates of the screen
        self.center_x = self.screen_width // 2.425
        self.center_y = self.screen_height // 1.943

        # Define the dimensions of the rectangular area
        self.area_width = 367
        self.area_height = 39

        #self.initUI() # Commented-out code is only used to get a visual of the location of the boxed area.
    '''
    def initUI(self):
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.setWindowTitle('Mouse Hover Guide')

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.screen_width, self.screen_height)

        self.showMaximized()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(255, 0, 0))  # Red color for the rectangle outline

        # Calculate the boundaries of the rectangular area
        left_boundary = int(self.center_x - self.area_width / 2)
        top_boundary = int(self.center_y - self.area_height / 2)

        # Draw the rectangle
        painter.drawRect(left_boundary, top_boundary, int(self.area_width), int(self.area_height))
    '''
    def is_mouse_over_center(self) -> tuple[bool, bool]:
        mouse_x, mouse_y = pyautogui.position()

        # Calculate the boundaries of the rectangular area
        left_boundary = self.center_x - self.area_width / 2
        right_boundary = self.center_x + self.area_width / 2
        top_boundary = self.center_y - self.area_height / 2
        bottom_boundary = self.center_y + self.area_height / 2

        # Check if the mouse coordinates are within the rectangular area
        return left_boundary <= mouse_x <= right_boundary and top_boundary <= mouse_y <= bottom_boundary

if __name__ == '__main__':
    app = QApplication(sys.argv)
    guide = RectangleGuide()
    
    while True:
        if guide.is_mouse_over_center():
            print("Mouse is over the selection field!")
            v('mouse_over_field', True)
            main() # Execute "mouse_speed.py" module
        else:
            print("Mouse is not over the selection field.")
            v('mouse_over_field', False)
        
        app.processEvents()
        
