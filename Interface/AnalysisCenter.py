from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class AnalysisCenter(QWidget):
    def __init__(self):
        
        self.Container = QWidget()
        self.Container.setObjectName('AnalysisCenter')
        
        top_layout = QVBoxLayout(self.Container)
        top_layout.setContentsMargins(50, 50, 50, 50)
        
        self.graph_label = QLabel('Graph', self.Container)
        self.graph_label.setObjectName('title')
        self.graph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.graph_label)
        
        self.graph_widget = QWidget(self.Container)
        self.graph_layout = QVBoxLayout(self.graph_widget)
        
        weight_layout = QVBoxLayout(self.Container)
        weightSettings = QLabel('Weight Monitor', self.Container)
        weightSettings.setObjectName('title')
        weight_layout.addWidget(weightSettings, alignment=Qt.AlignmentFlag.AlignTop)
        weight_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        
        self.weightLabel = QLabel('0.00', self.Container)
        self.weightLabel.setObjectName('weight')
        weight_layout.addWidget(self.weightLabel, alignment=Qt.AlignmentFlag.AlignLeft)
        
        flowRateTitle = QLabel('Flow Rate', self.Container)
        flowRateTitle.setObjectName('title')
        weight_layout.addWidget(flowRateTitle, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.flowRateLabel = QLabel('0.00', self.Container)
        self.flowRateLabel.setObjectName('weight')
        weight_layout.addWidget(self.flowRateLabel, alignment=Qt.AlignmentFlag.AlignLeft)

        
        self.tareScale = QPushButton('Tare Scale', self.Container)
        self.tareScale.setObjectName('tare')
        weight_layout.addWidget(self.tareScale, alignment=Qt.AlignmentFlag.AlignRight)
        
        top_layout.addWidget(self.graph_widget)
        top_layout.addLayout(weight_layout)