from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit
from PyQt6.QtCore import Qt, QTimer
from Controller.Nozzle import Nozzle
import time

class NozzleMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nozzle = Nozzle()
        
        self.setWindowTitle("Nozzle Menu")
        self.setGeometry(100, 100, 400, 300)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Current Position
        self.position_label = QLabel("Current Position:", self)
        self.position_label.setObjectName("title")
        self.layout.addWidget(self.position_label)
        
        self.position_value = QLabel(str(self.nozzle.position), self)
        self.position_value.setObjectName("label")
        self.layout.addWidget(self.position_value)
        self.position_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.default_position_button = QPushButton("Return to Home", self)
        self.default_position_button.clicked.connect(lambda: self.nozzle.move_to(0))
        self.layout.addWidget(self.default_position_button)
        
        self.set_home_button = QPushButton("Set Home", self)
        self.set_home_button.clicked.connect(self.set_home)
        self.layout.addWidget(self.set_home_button)
        
        self.central_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.central_widget.keyPressEvent = self.key_press_event
        self.central_widget.keyReleaseEvent = self.key_release_event
        
        self.right_key_pressed = False
        self.left_key_pressed = False
            
    def key_press_event(self, event):
        if event.key() == Qt.Key.Key_Right:
            if not self.right_key_pressed:
                self.right_key_pressed = True
                self.move_right()
                
        elif event.key() == Qt.Key.Key_Left:
            if not self.left_key_pressed:
                self.left_key_pressed = True
                self.move_left()
    
    def key_release_event(self, event):
        if event.key() == Qt.Key.Key_Right:
            self.right_key_pressed = False
            self.nozzle.stop()
            
        elif event.key() == Qt.Key.Key_Left:
            self.left_key_pressed = False
            self.nozzle.stop()

    def move_right(self):
        if self.right_key_pressed:
            self.nozzle.clockwise()
            self.update_position_label()
            QTimer.singleShot(5, self.move_right)
    
    def move_left(self):
        if self.left_key_pressed:
            self.nozzle.counter_clockwise()
            self.update_position_label()
            QTimer.singleShot(5, self.move_left)
    
    def update_position_label(self):
        self.position_value.setText(str(self.nozzle.position))
        
    def set_home(self):
        self.nozzle.position = 0
        self.position_value.setText(str(self.nozzle.position))
            