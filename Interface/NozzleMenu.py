from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit
from PyQt6.QtCore import Qt, QTimer
from Controller.Nozzle import Nozzle
from Controller.Controller import Controller
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
        
        self.input_layout = QVBoxLayout()
        
        self.up_button = QPushButton("Up", self)
        self.up_button.pressed.connect(self.start_moving_up)
        self.up_button.released.connect(self.stop)
        self.input_layout.addWidget(self.up_button, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.down_button = QPushButton("Down", self)
        self.down_button.pressed.connect(self.start_moving_down)
        self.down_button.released.connect(self.stop)
        self.input_layout.addWidget(self.down_button, alignment=Qt.AlignmentFlag.AlignBottom)
        
        self.layout.addLayout(self.input_layout)
        
        self.set_home_button = QPushButton("Set Home", self)
        self.set_home_button.clicked.connect(self.set_home)
        self.layout.addWidget(self.set_home_button)
        
        self.central_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.central_widget.keyPressEvent = self.key_press_event
        self.central_widget.keyReleaseEvent = self.key_release_event
        
        self.up_button_pressed = False
        self.down_button_pressed = False
            
    def key_press_event(self, event):
        # Handle key press events for arrow keys
        if event.key() == Qt.Key.Key_Up:
            if not self.up_button_pressed:
                self.up_button_pressed = True
                self.move_up()
        elif event.key() == Qt.Key.Key_Down:
            if not self.down_button_pressed:
                self.down_button_pressed = True
                self.move_down()
            
    
    def key_release_event(self, event):
        # Handle key release events for arrow keys
        if event.key() == Qt.Key.Key_Right:
            self.right_key_pressed = False
            self.stop()
            
        elif event.key() == Qt.Key.Key_Left:
            self.left_key_pressed = False
            self.stop()
            
    def start_moving_up(self):
        # Start moving the nozzle up
        if not self.up_button_pressed:
            self.up_button_pressed = True
            self.move_up()

    def move_up(self):
        # Move the nozzle up
        if self.up_button_pressed:
            self.nozzle.counter_clockwise()
            self.update_position_label()
            QTimer.singleShot(5, self.move_up)
        
    def start_moving_down(self):
        # Start moving the nozzle down
        if not self.down_button_pressed:
            self.down_button_pressed = True
            self.move_down()
    
    def move_down(self):
        # Move the nozzle down
        if self.down_button_pressed:
            self.nozzle.clockwise()
            self.update_position_label()
            QTimer.singleShot(5, self.move_down)
        
    def stop(self):
        # Stop the nozzle movement
        self.down_button_pressed = False
        self.up_button_pressed = False
        self.nozzle.stop()
        self.update_position_label()

    
    def update_position_label(self):
        # Update the position label with the current nozzle position
        self.position_value.setText(str(self.nozzle.position))
        
    def set_home(self):
        # Set the current position as the home position
        self.nozzle.set_home()
        self.position_value.setText(str(self.nozzle.position))
            