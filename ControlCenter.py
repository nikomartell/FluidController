from PyQt6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QComboBox, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QTimer, Qt
from calcs import setComponent, setFlowRate, setStrokes, setAcceleration, setFlowDirection, setDuration, setIterations

def create_control_center(controller):
    
    con = controller
    Container = QWidget()
    Container.setObjectName('ControlCenter')
    
    top_layout = QVBoxLayout(Container)
    top_layout.setContentsMargins(50, 10, 50, 10)
    
    device_layout = QHBoxLayout(Container)
    device_layout.setContentsMargins(0, 20, 0, 20)
    device_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
    
    motion_layout = QVBoxLayout(Container)
    motion_layout.setContentsMargins(0, 0, 30, 0)
    motionSettings = QLabel('Motion Settings', Container)
    motionSettings.setObjectName('title')
    motion_layout.addWidget(motionSettings, alignment=Qt.AlignmentFlag.AlignTop)
    motion_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
    end_case_layout = QVBoxLayout(Container)
    end_case_layout.setContentsMargins(0, 0, 30, 0)
    endCase = QLabel('End Case Settings', Container)
    endCase.setObjectName('title')
    end_case_layout.addWidget(endCase, alignment=Qt.AlignmentFlag.AlignTop)
    end_case_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
    weight_layout = QVBoxLayout(Container)
    weightSettings = QLabel('Weight Monitor', Container)
    weightSettings.setObjectName('title')
    weight_layout.addWidget(weightSettings, alignment=Qt.AlignmentFlag.AlignTop)
    weight_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
    button_layout = QHBoxLayout(Container)
    button_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
    
    #---------------------------------------------------------#
    
    #----------Motion Settings----------#
    
    # Component
    componentLabel = QLabel('Component:', Container)
    component = QComboBox()
    component.setObjectName('component')
    component.addItems(['Rotary Motor', 'Linear Motor'])
    
    componentLayout = QVBoxLayout()
    componentLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
    componentLayout.addWidget(componentLabel, alignment=Qt.AlignmentFlag.AlignTop)
    componentLayout.addWidget(component, alignment=Qt.AlignmentFlag.AlignTop)
    top_layout.addLayout(componentLayout)
    
    # Flow Rate
    flowRateLabel = QLabel('Flow Rate (Ml/sec):', Container)
    flowRate = QLineEdit()
    flowRate.setPlaceholderText('Default: 1.0')
    flowRate.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow only numbers with up to 2 decimal places
    
    flowRateLayout = QVBoxLayout()
    flowRateLayout.addWidget(flowRateLabel, alignment=Qt.AlignmentFlag.AlignTop)
    flowRateLayout.addWidget(flowRate, alignment=Qt.AlignmentFlag.AlignTop)
    motion_layout.addLayout(flowRateLayout)
    
    # Strokes
    strokesLabel = QLabel('Strokes(Rotations):', Container)
    strokes = QLineEdit()
    strokes.setPlaceholderText('Default: 10.0')
    strokes.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow only numbers with up to 2 decimal places
    
    strokesLayout = QVBoxLayout()
    strokesLayout.addWidget(strokesLabel, alignment=Qt.AlignmentFlag.AlignTop)
    strokesLayout.addWidget(strokes, alignment=Qt.AlignmentFlag.AlignTop)
    motion_layout.addLayout(strokesLayout)
    
    # Acceleration
    accelerationLabel = QLabel('Acceleration (Ml/sec^2):', Container)
    acceleration = QLineEdit()
    acceleration.setPlaceholderText('Default: 0.0')
    acceleration.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow only numbers with up to 2 decimal places
    
    accelerationLayout = QVBoxLayout()
    accelerationLayout.addWidget(accelerationLabel, alignment=Qt.AlignmentFlag.AlignTop)
    accelerationLayout.addWidget(acceleration, alignment=Qt.AlignmentFlag.AlignTop)
    motion_layout.addLayout(accelerationLayout)
    
    # Flow Direction
    flowDirectionLabel = QLabel('Flow Direction:', Container)
    flowDirection = QComboBox()
    flowDirection.addItems(['Dispense', 'Extract'])

    flowDirectionLayout = QVBoxLayout()
    flowDirectionLayout.addWidget(flowDirectionLabel, alignment=Qt.AlignmentFlag.AlignTop)
    flowDirectionLayout.addWidget(flowDirection, alignment=Qt.AlignmentFlag.AlignTop)
    motion_layout.addLayout(flowDirectionLayout)
    
    #----------End Case Settings----------#
    
    # Duration
    durationLabel = QLabel('Duration (Seconds):', Container)
    duration = QLineEdit()
    duration.setPlaceholderText('Default: 10.0')
    duration.setValidator(QDoubleValidator(0.0, 100.0, 2))  # Allow only numbers with up to 2 decimal places
    
    durationLayout = QVBoxLayout()
    durationLayout.addWidget(durationLabel, alignment=Qt.AlignmentFlag.AlignTop)
    durationLayout.addWidget(duration, alignment=Qt.AlignmentFlag.AlignTop)
    end_case_layout.addLayout(durationLayout)
    
    # Iterations
    iterationsLabel = QLabel('Iterations:', Container)
    iterations = QLineEdit()
    iterations.setPlaceholderText('Default: 10')
    iterations.setValidator(QDoubleValidator(0.0, 100.0, 0))  # Allow only numbers with up to 0 decimal places
    
    iterationsLayout = QVBoxLayout()
    iterationsLayout.addWidget(iterationsLabel, alignment=Qt.AlignmentFlag.AlignTop)
    iterationsLayout.addWidget(iterations, alignment=Qt.AlignmentFlag.AlignTop)
    end_case_layout.addLayout(iterationsLayout)
    
    #----------Weight Scale Settings----------#
    
    # Scale Control
    def update_weight():
        # This function should interact with the controller to get the current weight
        if con.scale is not None:
            scaleData = con.scale.get_weight()
            current_weight = f"{scaleData:.3f}"
        else:
            current_weight = "Scale not found"
        weightLabel.setText(f"{current_weight}")
    weightLabel = QLabel('', Container)
    weightLabel.setObjectName('weight')
    weight_layout.addWidget(weightLabel, alignment=Qt.AlignmentFlag.AlignCenter)
    timer = QTimer(Container)
    timer.timeout.connect(update_weight)
    timer.start(1000)  # Update every second
    
    tareScale = QPushButton('Tare Scale', Container)
    tareScale.setObjectName('tare')
    button_layout.addWidget(tareScale, alignment=Qt.AlignmentFlag.AlignRight)
    
    #---------------------------------------------------------#
    
    device_layout.addLayout(motion_layout)
    device_layout.addLayout(end_case_layout)
    device_layout.addLayout(weight_layout)
    
    top_layout.addLayout(device_layout)
    top_layout.addLayout(button_layout)
    
    # Send Commands from text boxes to device
    def get_commands():
        # Functions used for each variable translates input to commands
        componentCom = setComponent(component.currentText())
        flowRateCom = setFlowRate(flowRate.text())
        strokesCom = setStrokes(strokes.text())
        accelerationCom = setAcceleration(acceleration.text())
        flowDirectionCom = setFlowDirection(flowDirection.currentText())
        durationCom = setDuration(duration.text())
        iterationsCom = setIterations(iterations.text())
        
        commands = [setComponent(component.currentText()), flowRateCom, strokesCom, accelerationCom, flowDirectionCom, durationCom, iterationsCom]
        
        return commands
    
    def set_commands(commands):
        component.setCurrentText(commands[0])
        flowRate.setText(commands[1])
        strokes.setText(commands[2])
        acceleration.setText(commands[3])
        flowDirection.setCurrentText(commands[4])
        duration.setText(commands[5])
        iterations.setText(commands[6])
    
    Container.get_commands = get_commands
    Container.set_commands = set_commands
    return Container