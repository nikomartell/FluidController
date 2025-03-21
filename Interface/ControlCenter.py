from PyQt6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QComboBox, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QTimer, Qt
from Controller.CommandSet import CommandSet

class controlCenter(QWidget):
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
        
        # self.Component
        componentLabel = QLabel('Component:', self.Container)
        self.component = QComboBox()
        self.component.setObjectName('self.component')
        self.component.addItems(['Linear Motor', 'Rotary Motor'])
        
        componentLayout = QVBoxLayout()
        componentLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        componentLayout.addWidget(componentLabel, alignment=Qt.AlignmentFlag.AlignTop)
        componentLayout.addWidget(self.component, alignment=Qt.AlignmentFlag.AlignTop)
        top_layout.addLayout(componentLayout)
        
        # Flow Rate
        flowRateLabel = QLabel('Flow Rate (Ml/sec):', self.Container)
        self.flowRate = QLineEdit()
        self.flowRate.setPlaceholderText('Default: 1.0')
        self.flowRate.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow only numbers with up to 2 decimal places
        
        flowRateLayout = QVBoxLayout()
        flowRateLayout.addWidget(flowRateLabel, alignment=Qt.AlignmentFlag.AlignTop)
        flowRateLayout.addWidget(self.flowRate, alignment=Qt.AlignmentFlag.AlignTop)
        motion_layout.addLayout(flowRateLayout)
        
        # Strokes
        strokesLabel = QLabel('Strokes(Rotations):', self.Container)
        self.strokes = QLineEdit()
        self.strokes.setPlaceholderText('Default: 10.0')
        self.strokes.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow only numbers with up to 2 decimal places
        
        strokesLayout = QVBoxLayout()
        strokesLayout.addWidget(strokesLabel, alignment=Qt.AlignmentFlag.AlignTop)
        strokesLayout.addWidget(self.strokes, alignment=Qt.AlignmentFlag.AlignTop)
        motion_layout.addLayout(strokesLayout)
        
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
        self.flowDirection = QComboBox()
        self.flowDirection.addItems(['Dispense', 'Aspirate'])

        flowDirectionLayout = QVBoxLayout()
        flowDirectionLayout.addWidget(flowDirectionLabel, alignment=Qt.AlignmentFlag.AlignTop)
        flowDirectionLayout.addWidget(self.flowDirection, alignment=Qt.AlignmentFlag.AlignTop)
        motion_layout.addLayout(flowDirectionLayout)
        
        #----------End Case Settings----------#
        
        # Duration
        durationLabel = QLabel('Duration (Seconds):', self.Container)
        self.duration = QLineEdit()
        self.duration.setPlaceholderText('Default: 10.0')
        self.duration.setValidator(QDoubleValidator(0.0, 100.0, 0))  # Allow only integers
        
        durationLayout = QVBoxLayout()
        durationLayout.addWidget(durationLabel, alignment=Qt.AlignmentFlag.AlignTop)
        durationLayout.addWidget(self.duration, alignment=Qt.AlignmentFlag.AlignTop)
        end_case_layout.addLayout(durationLayout)
        
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
        componentCom = self.component.currentText()
        flowRateCom = self.flowRate.text()
        strokesCom = self.strokes.text()
        accelerationCom = self.acceleration.text()
        flowDirectionCom = self.flowDirection.currentText()
        durationCom = self.duration.text()
        iterationsCom = self.iterations.text()
        
        commands = CommandSet(componentCom, flowRateCom, strokesCom, accelerationCom, 
                              flowDirectionCom, durationCom, iterationsCom)
            
        return commands
        
    def set_commands(self, commandSet):
        self.component.setCurrentText(commandSet.component)
        self.flowRate.setText(commandSet.flowRate)
        self.strokes.setText(commandSet.strokes)
        self.acceleration.setText(commandSet.acceleration)
        self.flowDirection.setCurrentText(commandSet.flowDirection)
        self.duration.setText(commandSet.duration)
        self.iterations.setText(commandSet.iterations)
        
        