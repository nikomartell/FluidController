from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QDoubleValidator, QIntValidator
from Controller.Controller import Controller

class CalibrationMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        if isinstance(parent.device, Controller):
            
            self.controller = parent.device
            self.rotary = parent.device.rotary
            self.limit = 0
            self.searching = False
            
            self.setWindowTitle("Calibration Menu")
            self.setGeometry(100, 100, 400, 300)
            
            self.central_widget = QWidget(self)
            self.setCentralWidget(self.central_widget)
            
            self.layout = QVBoxLayout(self.central_widget)
            
            # Title
            self.title_label = QLabel("Calibration Menu", self)
            self.title_label.setObjectName("title")
            self.title_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.layout.addWidget(self.title_label)
            
            # Current Position
            self.current_position_label = QLabel("Current Position:", self)
            self.current_position_label.setObjectName("label")
            self.layout.addWidget(self.current_position_label)
            
            self.position_label = QLabel(self.rotary.actual_position, self)
            self.position_label.setObjectName("label")
            self.layout.addWidget(self.position_label)
            
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
            self.set_home
            
        self.position_label.setText(str(self.rotary.acutal_position))

    def key_release_event(self, event):
        if event.key() == Qt.Key.Key_Right:
            self.right_key_pressed = False
        elif event.key() == Qt.Key.Key_Left:
            self.left_key_pressed = False
        
        self.rotary.stop()


    def start_moving_right(self):
        if self.right_key_pressed:
            self.move_right()
            QTimer.singleShot(10, self.start_moving_right)  # Repeat every 10ms
    
    def start_moving_left(self):
        if self.left_key_pressed:
            self.move_left()
            QTimer.singleShot(10, self.start_moving_left)
    
    
    def move_right(self):
        # rotate the motor clockwise
        try:
            self.rotary.rotate(-5)
        except Exception as e:
            print(f'Error: {e}')
    
    def move_left(self):
        # rotate the motor counter-clockwise
        try:
            self.rotary.rotate(5)
        except Exception as e:
            print(f'Error: {e}')
            
    def set_home(self):
        try:
            if self.searching:
                # Set the home position to 0 and user to complete one full rotation
                self.searching = True
                self.rotary.acutal_position = 0
            elif self.searching == False:
                # Set the upper limit position that completes the rotation
                self.searching = False
                excess = self.rotary.acutal_position % self.rotary.drive_settings.get_microstep_resolution()
                self.limit = self.rotary.acutal_position - excess
                
                # Move to the limit position to ensure no excess microsteps in position
                self.rotary.move_to(self.limit)
                self.rotary.acutal_position = 0
                
                self.controller.set_rotary_home(self.limit)
                QMessageBox.information(self, "Set Home", "Home position set successfully!")
                
        except Exception as e:
            print(f'Error: {e}')
            QMessageBox.critical(self, "Error", f"Failed to set home position: {e}")