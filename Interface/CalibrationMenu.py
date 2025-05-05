from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QDoubleValidator, QIntValidator
from Controller.Controller import Controller
import time

class CalibrationMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        if isinstance(parent.device, Controller):
            
            self.controller = parent.device
            self.rotary = parent.device.rotary
            
            self.setWindowTitle("Calibration Menu")
            self.setGeometry(100, 100, 400, 300)
            
            self.central_widget = QWidget(self)
            self.setCentralWidget(self.central_widget)
            
            self.layout = QVBoxLayout(self.central_widget)
            
            # Current Position
            self.current_position_label = QLabel("Current Position:", self)
            self.current_position_label.setObjectName("title")
            self.layout.addWidget(self.current_position_label)
            
            self.position_label = QLabel(str(self.rotary.actual_position), self)
            self.position_label.setObjectName("label")
            self.layout.addWidget(self.position_label)
            
            self.input_layout = QHBoxLayout()
            
            self.left_button = QPushButton("←", self)
            self.left_button.pressed.connect(self.start_moving_left)
            self.left_button.released.connect(self.stop)
            self.left_button.setStyleSheet("font-size: 24px")
            self.input_layout.addWidget(self.left_button)
            
            
            self.right_button = QPushButton("→", self)
            self.right_button.pressed.connect(self.start_moving_right)
            self.right_button.released.connect(self.stop)
            self.right_button.setStyleSheet("font-size: 24px")
            self.input_layout.addWidget(self.right_button)
            
            
            self.layout.addLayout(self.input_layout)
            
            # Calibration Button
            self.calibration_button = QPushButton("Set Home", self)
            self.calibration_button.clicked.connect(self.set_home)
            self.layout.addWidget(self.calibration_button)
            
            # Key Press Event
            self.central_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self.central_widget.keyPressEvent = self.key_press_event
            self.central_widget.keyReleaseEvent = self.key_release_event

            self.right_key_pressed = False
            self.left_key_pressed = False

    def key_press_event(self, event):
        # Right key moves the motor clockwise
        # Left key moves the motor counter-clockwise
        # Space key sets the home position
        if event.key() == Qt.Key.Key_Right:
            if not self.right_key_pressed:
                self.right_key_pressed = True
                self.start_moving_right()
                
        elif event.key() == Qt.Key.Key_Left:
            if not self.left_key_pressed:
                self.left_key_pressed = True
                self.start_moving_left()
                
        elif event.key() == Qt.Key.Key_Space:
            self.set_home()
            
            
    def key_release_event(self, event):
        # When an arrow key is released, stop the motor from rotating
        if event.key() == Qt.Key.Key_Right:
            self.right_key_pressed = False
            self.rotary.stop()
            self.position_label.setText(str(self.rotary.actual_position))
        elif event.key() == Qt.Key.Key_Left:
            self.left_key_pressed = False
            self.rotary.stop()
            self.position_label.setText(str(self.rotary.actual_position))


    def start_moving_right(self):
        if not self.right_key_pressed:
            self.right_key_pressed = True
            self.move_right()
    
    def start_moving_left(self):
        if not self.left_key_pressed:
            self.left_key_pressed = True
            self.move_left()
    
    
    def move_right(self):
        # rotate the motor clockwise
        try:
            if self.right_key_pressed:
                self.rotary.rotate(-10)
                self.position_label.setText(str(self.rotary.actual_position))
                QTimer.singleShot(5, self.move_right)
        except Exception as e:
            print(f'Error: {e}')
    
    def move_left(self):
        # rotate the motor counter-clockwise
        try:
            if self.left_key_pressed:
                self.rotary.rotate(10)
                self.position_label.setText(str(self.rotary.actual_position))
                QTimer.singleShot(5, self.move_left)
        except Exception as e:
            print(f'Error: {e}')
    
    def stop(self):
        # Stop the motor
        self.right_key_pressed = False
        self.left_key_pressed = False
        self.rotary.stop()
        self.position_label.setText(str(self.rotary.actual_position))
            
    def set_home(self):
        try:
            self.rotary.set_actual_position(0)
            QMessageBox.information(self, "Set Home", "Home position set successfully!")
                
        except Exception as e:
            print(f'Error: {e}')
            QMessageBox.critical(self, "Error", f"Failed to set home position: {e}")