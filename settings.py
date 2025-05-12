from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        coming_soon_label = QLabel("🚧 Settings Coming Soon")
        coming_soon_label.setFont(QFont("Segoe UI Emoji", 18, QFont.Bold))
        coming_soon_label.setStyleSheet("""
            QLabel {
                color: #ffa500;
                padding: 20px;
                border: 2px dashed #ffa500;
                border-radius: 15px;
                background-color: rgba(255, 165, 0, 0.1);
            }
        """)
        coming_soon_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(coming_soon_label)
        self.setLayout(layout)
