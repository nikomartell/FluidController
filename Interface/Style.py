from PyQt6 import QtGui

def apply_style(parent):
    QtGui.QFontDatabase.addApplicationFont("Interface/RocheSans.ttf")
    parent.setStyleSheet("""
        QWidget {
            background-color: #f0f0f0;
            color: black;
            font-family: 'RocheSans';
            font-size: 16px;
        }

        QWidget#ControlCenter {
            background-color: #f0f0f0;
            color: black;
            font-family: 'RocheSans';
            font-size: 16px;
            border: 2px solid #0B41CD;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            border-bottom-left-radius: 5px;
        }

        QWidget#AnalysisCenter {
            background-color: #f0f0f0;
            color: black;
            font-family: 'RocheSans';
            font-size: 16px;
        }

        QPushButton {
            background-color: #545860;
            color: #ffffff;
            border: 2px solid #545860;
            border-radius: 5px;
            max-width: 200px;
            max-height: 120px;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
        }
        
        QWidget#menubar {
            background-color: #545860;
            color: #ffffff;
            font-size: 16px;
        }

        QPushButton#barbutton {
            border: 0px;
            border-bottom: 5px solid qlineargradient(x1:0, y1:1, x2:0, y2:0,
                stop:0.1 #0B41CD, stop: 1 transparent, stop:1 transparent);
        }
        
        QPushButton:pressed {
            background-color: #0B41CD;
            color: #ffffff;
        }
        
        QPushButton#small {
            width: 40px;
            height: 25px;
            padding: 5px;
            font-size: 24px;
        }

        QLabel {
            border: #f0f0f0;
        }
        
        QLabel#error {
            color: #b60000;
            font-size: 16px;
            font-weight: bold;
        }

        QLabel#device_info {
            font-size: 16px;
            position: absolute;
        }

        QLabel#title{
            font-size: 20px;
            font-weight: bold;
        }

        QLabel#weight {
            font-size: 26px;
            font-weight: bold;
        }
        
        QLabel#error {
            font-size: 16px;
            color: red;
            font-weight: bold;
        }
        
        QLineEdit {
            border: 1px solid #333333;
            border-radius: 5px;
            padding: 5px;
            background-color: #ffffff;
            height: 30%;
            width: 100px;
        }

        QComboBox {
            background-color: #ffffff;
            border: 1px solid #333333;
            padding: 5px;
            max-width: 200px;
            height: 30%;
            width: 150%;
        }

        QComboBox QAbstractItemView {
            background-color: #ffffff;
            border: 1px solid #333333;
            border-radius: 5px;
        }

        QComboBox QAbstractItemView::item:selected {
            background-color: #0B41CD;
            color: #ffffff;
        }

        QComboBox#component {
            border: 2px solid #0B41CD;
            border-radius: 5px;
            padding: 5px;
        }
        
        QTabWidget::pane {
            
        }
        
        QTabBar::tab {
            background-color: #ffffff;
            padding: 10px;
            border: 2px solid #0B41CD;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        
        QTabBar::tab:selected {
            background-color: #0B41CD;
            color: #ffffff;
        }
        
        QTabBar::tab:!selected {
            margin-top: 2px;
        }
    """)