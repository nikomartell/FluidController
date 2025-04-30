from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QBoxLayout
from PyQt6.QtCore import Qt, QTimer
from Controller.Nozzle import Nozzle
from Controller.Controller import Controller
import time

class NozzleMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nozzle = Nozzle()
        if isinstance(parent, Controller):
            self.positioner = parent.positioner
        
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
        
        self.input_layout = QBoxLayout()
            
        self.left_button = QPushButton("Left", self)
        self.left_button.clicked.connect(self.move_left)
        self.left_button.released.connect(self.nozzle.stop)
        self.input_layout.addWidget(self.left_button, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.right_button = QPushButton("Right", self)
        self.right_button.clicked.connect(self.move_right)
        self.right_button.released.connect(self.nozzle.stop)
        self.input_layout.addWidget(self.right_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.up_button = QPushButton("Up", self)
        self.up_button.clicked.connect(self.move_up)
        self.up_button.released.connect(self.positioner.stop)
        self.input_layout.addWidget(self.up_button, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.down_button = QPushButton("Down", self)
        self.down_button.clicked.connect(self.move_down)
        self.down_button.released.connect(self.positioner.stop)
        self.input_layout.addWidget(self.down_button, alignment=Qt.AlignmentFlag.AlignBottom)
        
        self.layout.addLayout(self.input_layout)
        
        self.set_home_button = QPushButton("Set Home", self)
        self.set_home_button.clicked.connect(self.set_home)
        self.layout.addWidget(self.set_home_button)
        
        self.central_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.central_widget.keyPressEvent = self.key_press_event
        self.central_widget.keyReleaseEvent = self.key_release_event
        
        self.right_key_pressed = False
        self.left_key_pressed = False
        self.up_key_pressed = False
        self.down_key_pressed = False
            
    def key_press_event(self, event):
        # Handle key press events for arrow keys
        if event.key() == Qt.Key.Key_Right:
            if not self.right_key_pressed:
                self.right_key_pressed = True
                self.move_right()
                
        elif event.key() == Qt.Key.Key_Left:
            if not self.left_key_pressed:
                self.left_key_pressed = True
                self.move_left()
        elif event.key() == Qt.Key.Key_Up:
            if not self.up_key_pressed:
                self.up_key_pressed = True
                self.move_up()
        elif event.key() == Qt.Key.Key_Down:
            if not self.down_key_pressed:
                self.down_key_pressed = True
                self.move_down()
            
    
    def key_release_event(self, event):
        # Handle key release events for arrow keys
        if event.key() == Qt.Key.Key_Right:
            self.right_key_pressed = False
            self.nozzle.stop()
            
        elif event.key() == Qt.Key.Key_Left:
            self.left_key_pressed = False
            self.nozzle.stop()
        
        elif event.key() == Qt.Key.Key_Up:
            self.up_key_pressed = False
            self.positioner.stop()
        
        elif event.key() == Qt.Key.Key_Down:
            self.down_key_pressed = False
            self.positioner.stop()

    def move_up(self):
        # Move the nozzle up
        self.nozzle.clockwise()
        self.update_position_label()
        QTimer.singleShot(5, self.move_up)
    
    def move_down(self):
        # Move the nozzle down
        self.nozzle.counter_clockwise()
        self.update_position_label()
        QTimer.singleShot(5, self.move_down)
        
    def move_left(self):
        # Move the positioner to the left
        self.positioner.move_by(5, velocity=50)
        self.update_position_label()
        QTimer.singleShot(5, self.move_left)
    
    def move_right(self):
        # Move the positioner to the right
        self.positioner.move_by(-5, velocity=50)
        self.update_position_label()
        QTimer.singleShot(5, self.move_right)

    
    def update_position_label(self):
        # Update the position label with the current nozzle position
        self.position_value.setText(str(self.nozzle.position))
        
    def set_home(self):
        # Set the current position as the home position
        self.nozzle.position = 0
        self.position_value.setText(str(self.nozzle.position))
            