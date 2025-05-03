from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QBoxLayout, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt

class Keyboard(QWidget):
    def __init__(self):
        super().__init__()
        # Create a widget for the keyboard
        self.keyboard_widget = QWidget()
        keyboard_layout = QVBoxLayout(self.keyboard_widget)
        self.keyboard_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Create rows for the keyboard
        rows = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [0]
        ]

        for row in rows:
            row_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
            for digit in row:
                button = QPushButton(str(digit))
                button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                button.setFixedSize(40, 40)
                button.clicked.connect(lambda _, d=digit: self.insert_digit(d))
                row_layout.addWidget(button)
                keyboard_layout.addLayout(row_layout)
        
        # Add a backspace button
        backspace_button = QPushButton("⌫")
        backspace_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        backspace_button.setFixedSize(40, 40)
        backspace_button.clicked.connect(self.backspace)
        keyboard_layout.addWidget(backspace_button)
        
        # Add a negative button
        negative_button = QPushButton("±")
        negative_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        negative_button.setFixedSize(40, 40)
        negative_button.clicked.connect(self.toggle_negative)
        keyboard_layout.addWidget(negative_button)

        self.keyboard_widget.setLayout(keyboard_layout)

    def insert_digit(self, digit):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.insert(str(digit))
    
    def backspace(self):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.backspace()
            
    def toggle_negative(self):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            text = focused_widget.text()
            if text.startswith('-'):
                focused_widget.setText(text[1:])
            else:
                focused_widget.setText('-' + text)