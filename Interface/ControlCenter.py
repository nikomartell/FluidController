from PyQt6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QComboBox, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QTimer, Qt
from Controller.CommandSet import CommandSet

class ControlCenter(QWidget):
    def __init__(self):
        
        
        self.Container = QWidget()
        self.Container.setObjectName('ControlCenter')
        
        top_layout = QVBoxLayout(self.Container)
        top_layout.setContentsMargins(50, 10, 50, 10)
        
        device_layout = QHBoxLayout(self.Container)
        device_layout.setContentsMargins(0, 20, 0, 20)
        device_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Section Titles and creation
        
        motion_layout = QVBoxLayout(self.Container)
        motion_layout.setContentsMargins(0, 0, 30, 0)
        motionSettings = QLabel('Motion Settings', self.Container)
        motionSettings.setObjectName('title')
        motion_layout.addWidget(motionSettings, alignment=Qt.AlignmentFlag.AlignTop)
        motion_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        end_case_layout = QVBoxLayout(self.Container)
        end_case_layout.setContentsMargins(0, 0, 30, 0)
        endCase = QLabel('End Case Settings', self.Container)
        endCase.setObjectName('title')
        end_case_layout.addWidget(endCase, alignment=Qt.AlignmentFlag.AlignTop)
        end_case_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        button_layout = QHBoxLayout(self.Container)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        #---------------------------------------------------------#
        
        #----------Motion Settings----------#
        
        # Component
        componentLabel = QLabel('Component:', self.Container)
        self.component = QComboBox()
        self.component.setObjectName('self.component')
        self.component.addItems(['Rotary Motor'])
        
        componentLayout = QVBoxLayout()
        componentLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        componentLayout.addWidget(componentLabel, alignment=Qt.AlignmentFlag.AlignTop)
        componentLayout.addWidget(self.component, alignment=Qt.AlignmentFlag.AlignTop)
        top_layout.addLayout(componentLayout)
        
        # Flow Rate
        speedLabel = QLabel('Speed (RPM):', self.Container)
        self.speed = QLineEdit()
        self.speed.setPlaceholderText('Default: 500')
        self.speed.setValidator(QDoubleValidator(0.0, 100.0, 0))  # Allow only integers
        
        speedLayout = QVBoxLayout()
        speedLayout.addWidget(speedLabel, alignment=Qt.AlignmentFlag.AlignTop)
        speedLayout.addWidget(self.speed, alignment=Qt.AlignmentFlag.AlignTop)
        motion_layout.addLayout(speedLayout)
        
        
        # Acceleration
        accelerationLabel = QLabel('Acceleration (Ml/sec^2):', self.Container)
        self.acceleration = QLineEdit()
        self.acceleration.setPlaceholderText('Default: 0.0')
        self.acceleration.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow only numbers with up to 2 decimal places
        
        accelerationLayout = QVBoxLayout()
        accelerationLayout.addWidget(accelerationLabel, alignment=Qt.AlignmentFlag.AlignTop)
        accelerationLayout.addWidget(self.acceleration, alignment=Qt.AlignmentFlag.AlignTop)
        motion_layout.addLayout(accelerationLayout)
        
        # Flow Direction
        flowDirectionLabel = QLabel('Flow Direction:', self.Container)
        self.flow_direction = QComboBox()
        self.flow_direction.addItems(['Dispense', 'Aspirate'])

        flowDirectionLayout = QVBoxLayout()
        flowDirectionLayout.addWidget(flowDirectionLabel, alignment=Qt.AlignmentFlag.AlignTop)
        flowDirectionLayout.addWidget(self.flow_direction, alignment=Qt.AlignmentFlag.AlignTop)
        motion_layout.addLayout(flowDirectionLayout)
        
        #----------End Case Settings----------#
        
        # Duration
        durationLabel = QLabel('Duration (Seconds):', self.Container)
        self.duration = QLineEdit()
        self.duration.setPlaceholderText('Default: 5')
        self.duration.setValidator(QDoubleValidator(0.0, 100.0, 0))  # Allow only integers
        
        durationLayout = QVBoxLayout()
        durationLayout.addWidget(durationLabel, alignment=Qt.AlignmentFlag.AlignTop)
        durationLayout.addWidget(self.duration, alignment=Qt.AlignmentFlag.AlignTop)
        end_case_layout.addLayout(durationLayout)
        
        # Strokes
        strokesLabel = QLabel('Strokes(Rotations):', self.Container)
        self.strokes = QLineEdit()
        self.strokes.setPlaceholderText('Default: 0')
        self.strokes.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow only numbers with up to 2 decimal places
        
        strokesLayout = QVBoxLayout()
        strokesLayout.addWidget(strokesLabel, alignment=Qt.AlignmentFlag.AlignTop)
        strokesLayout.addWidget(self.strokes, alignment=Qt.AlignmentFlag.AlignTop)
        end_case_layout.addLayout(strokesLayout)
        
        # Iterations
        iterationsLabel = QLabel('Iterations:', self.Container)
        self.iterations = QLineEdit()
        self.iterations.setPlaceholderText('Default: 1')
        self.iterations.setValidator(QDoubleValidator(0.0, 100.0, 0))  # Allow only numbers with up to 0 decimal places
        
        iterationsLayout = QVBoxLayout()
        iterationsLayout.addWidget(iterationsLabel, alignment=Qt.AlignmentFlag.AlignTop)
        iterationsLayout.addWidget(self.iterations, alignment=Qt.AlignmentFlag.AlignTop)
        end_case_layout.addLayout(iterationsLayout)        
        
        #---------------------------------------------------------#
        
        device_layout.addLayout(motion_layout)
        device_layout.addLayout(end_case_layout)
        
        top_layout.addLayout(device_layout)
        top_layout.addLayout(button_layout)
        
        
        # Send Commands from text boxes to device
    def get_commands(self):
        # Functions used for each variable translates input to commands
        component = self.component.currentText()
        speed = self.speed.text()
        strokes = self.strokes.text()
        acceleration = self.acceleration.text()
        flow_direction = self.flow_direction.currentText()
        duration = self.duration.text()
        iterations = self.iterations.text()
        
        commands = CommandSet(component, speed, strokes, acceleration, 
                              flow_direction, duration, iterations)
            
        return commands
        
    def set_commands(self, command):
        if isinstance(command, CommandSet):
            self.component.setCurrentText(command.component)
            self.speed.setText(command.speed)
            self.strokes.setText(command.strokes)
            self.acceleration.setText(command.acceleration)
            self.flow_direction.setCurrentText(command.flow_direction)
            self.duration.setText(command.duration)
            self.iterations.setText(command.iterations)
        
        