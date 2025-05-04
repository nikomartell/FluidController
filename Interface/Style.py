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
            max-width: 400px;
            padding: 10px;
            font-size: 20px;
            font-weight: bold;
        }
        
        QPushButton:pressed {
            background-color: #0B41CD;
            color: #ffffff;
        }

        QPushButton#tare {
            max-width: 200px;
            max-height: 120px;
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
        
        QTabBar::tab {
            background-color: #ffffff;
            padding: 10px;
            border: 2px solid #0B41CD;
        }
        
        QTabBar::tab:selected {
            background-color: #0B41CD;
            color: #ffffff;
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

        QWidget#menubar {
            background-color: #545860;
            color: #ffffff;
            border: 2px solid #545860;
            border-radius: 0px;
            font-size: 20px;
            margin: 0px;
        }

        QWidget#menubar::item {
            background-color: #545860;
            color: #ffffff;
            font-size: 20px;
            padding: 5px;
        }

        QWidget#menubar::item:selected {
            background-color: #0B41CD;
            color: #ffffff;
        }

        QMenu {
            background-color: #545860;
            color: #ffffff;
            border: 0px;
            font-size: 20px;
            padding: 5px;
        }
        
        QMenu::item {
            padding: 5px;
        }

        QMenu::item:selected {
            background-color: #0B41CD;
            color: #ffffff;
        }
    """)