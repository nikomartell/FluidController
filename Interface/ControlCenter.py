from PyQt6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QComboBox, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QTimer, Qt
from Controller.CommandSet import CommandSet

class ControlCenter(QWidget):
    def __init__(self):
        QLineEdit.focusPolicy = Qt.FocusPolicy.ClickFocus
        
        self.Container = QWidget()
        self.Container.setFixedSize(500, 500)  # Set static size for the container
        self.Container.setObjectName('ControlCenter')
        
        top_layout = QVBoxLayout(self.Container)
        top_layout.setContentsMargins(30, 10, 30, 10)
        
        device_layout = QHBoxLayout(self.Container)
        device_layout.setContentsMargins(0, 20, 0, 20)
        device_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Section Titles and creation
        
        self.motion_layout = QVBoxLayout(self.Container)
        self.motion_layout.setContentsMargins(0, 0, 10, 0)
        motionSettings = QLabel('Motion Settings', self.Container)
        motionSettings.setObjectName('title')
        self.motion_layout.addWidget(motionSettings, alignment=Qt.AlignmentFlag.AlignTop)
        self.motion_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.end_case_layout = QVBoxLayout(self.Container)
        self.end_case_layout.setContentsMargins(0, 0, 10, 0)
        endCase = QLabel('End Case Settings', self.Container)
        endCase.setObjectName('title')
        self.end_case_layout.addWidget(endCase, alignment=Qt.AlignmentFlag.AlignTop)
        self.end_case_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        button_layout = QHBoxLayout(self.Container)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        #---------------------------------------------------------#
        
        #----------Motion Settings----------#
        
        self.set_motion_layout()
        
        #----------End Case Settings----------#
        
        self.set_end_case_layout()
        
        #---------------------------------------------------------#
        
        device_layout.addLayout(self.motion_layout)
        device_layout.addLayout(self.end_case_layout)
        
        top_layout.addLayout(device_layout)
        top_layout.addLayout(button_layout)
        
        
        # Send Commands from text boxes to device
    def get_commands(self):
        # Functions used for each variable translates input to commands
        speed = self.speed.text()
        strokes = self.strokes.text()
        acceleration = self.acceleration.text()
        flow_direction = self.flow_direction.text()
        duration = self.duration.text()
        iterations = self.iterations.text()
        position = self.linear_position.text()
        
        commands = CommandSet(speed, strokes, acceleration, 
                              flow_direction, duration, iterations, position)
            
        return commands
        
    def set_commands(self, command):
        if isinstance(command, CommandSet):
            self.speed.setText(command.speed)
            self.strokes.setText(command.strokes)
            self.acceleration.setText(command.acceleration)
            self.flow_direction.setText(command.flow_direction)
            self.duration.setText(command.duration)
            self.iterations.setText(command.iterations)
            self.linear_position.setText(command.position)
            
    
    def set_motion_layout(self):
        
        # Flow Rate
        speedLabel = QLabel('Speed (RPM):', self.Container)
        self.speed = QLineEdit()
        self.speed.setPlaceholderText('0 - 1500')
        self.speed.setValidator(QDoubleValidator(0.0, 1500.0, 0))  # Allow only positive integers
        
        speedLayout = QVBoxLayout()
        speedLayout.addWidget(speedLabel, alignment=Qt.AlignmentFlag.AlignTop)
        speedLayout.addWidget(self.speed, alignment=Qt.AlignmentFlag.AlignTop)
        self.motion_layout.addLayout(speedLayout)
        
        
        # Acceleration
        accelerationLabel = QLabel('Acceleration (Ml/sec^2):', self.Container)
        self.acceleration = QLineEdit()
        self.acceleration.setPlaceholderText('0 - 2000')
        self.acceleration.setValidator(QDoubleValidator(0.0, 2000.0, 0))  # Allow only integers
        
        accelerationLayout = QVBoxLayout()
        accelerationLayout.addWidget(accelerationLabel, alignment=Qt.AlignmentFlag.AlignTop)
        accelerationLayout.addWidget(self.acceleration, alignment=Qt.AlignmentFlag.AlignTop)
        self.motion_layout.addLayout(accelerationLayout)
        
        # Flow Direction
        flowDirectionLabel = QLabel('Flow Direction:', self.Container)
        self.flow_direction = QPushButton('Dispense', self.Container)
        self.flow_direction.setCheckable(True)
        self.flow_direction.clicked.connect(lambda: self.toggle_flow_direction())

        flowDirectionLayout = QVBoxLayout()
        flowDirectionLayout.addWidget(flowDirectionLabel, alignment=Qt.AlignmentFlag.AlignTop)
        flowDirectionLayout.addWidget(self.flow_direction, alignment=Qt.AlignmentFlag.AlignTop)
        self.motion_layout.addLayout(flowDirectionLayout)
        
        # linear Position
        linearPositionLabel = QLabel('Linear Position:', self.Container)
        self.linear_position = QLineEdit()
        self.linear_position.setPlaceholderText('0 - 42000')
        self.linear_position.setValidator(QDoubleValidator(0.0, 100.0, 0)) # Allow only integers
        
        linearPositionLayout = QVBoxLayout()
        linearPositionLayout.addWidget(linearPositionLabel, alignment=Qt.AlignmentFlag.AlignTop)
        linearPositionLayout.addWidget(self.linear_position, alignment=Qt.AlignmentFlag.AlignTop)
        self.motion_layout.addLayout(linearPositionLayout)
        
        
    def set_end_case_layout(self):
        
        # Duration
        durationLabel = QLabel('Duration (Seconds):', self.Container)
        self.duration = QLineEdit()
        self.duration.setPlaceholderText('Default: 5')
        self.duration.setValidator(QDoubleValidator(0.0, 10.0, 2))  # Allow only numbers with up to 2 decimal places
        
        durationLayout = QVBoxLayout()
        durationLayout.addWidget(durationLabel, alignment=Qt.AlignmentFlag.AlignTop)
        durationLayout.addWidget(self.duration, alignment=Qt.AlignmentFlag.AlignTop)
        self.end_case_layout.addLayout(durationLayout)
        
        # Strokes
        strokesLabel = QLabel('Strokes (Rotations):', self.Container)
        self.strokes = QLineEdit()
        self.strokes.setPlaceholderText('Default: 0')
        self.strokes.setValidator(QDoubleValidator(0.0, 100.0, 0))  # Allow only integers
        
        strokesLayout = QVBoxLayout()
        strokesLayout.addWidget(strokesLabel, alignment=Qt.AlignmentFlag.AlignTop)
        strokesLayout.addWidget(self.strokes, alignment=Qt.AlignmentFlag.AlignTop)
        self.end_case_layout.addLayout(strokesLayout)
        
        # Iterations
        iterationsLabel = QLabel('Iterations:', self.Container)
        self.iterations = QLineEdit()
        self.iterations.setPlaceholderText('Default: 1')
        self.iterations.setValidator(QDoubleValidator(0.0, 100.0, 0))  # Allow only integers
        
        iterationsLayout = QVBoxLayout()
        iterationsLayout.addWidget(iterationsLabel, alignment=Qt.AlignmentFlag.AlignTop)
        iterationsLayout.addWidget(self.iterations, alignment=Qt.AlignmentFlag.AlignTop)
        self.end_case_layout.addLayout(iterationsLayout) 
        
    def toggle_flow_direction(self):
        if self.flow_direction.isChecked():
            self.flow_direction.setText('Aspirate')
        else:
            self.flow_direction.setText('Dispense')