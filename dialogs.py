from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QApplication
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class ImagePreviewDialog(QDialog):
    def __init__(self, image_paths, current_index=0, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🖼️ Image Preview")
        self.setFixedSize(900, 700)
        self.image_paths = image_paths
        self.current_index = current_index

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(860, 580)
        self.label.setStyleSheet("""
            QLabel {
                background-color: #2e2e2e;
                border: 2px solid #444;
                border-radius: 10px;
            }
        """)

        self.position_label = QLabel()
        self.position_label.setAlignment(Qt.AlignCenter)
        self.position_label.setStyleSheet("color: white; font-size: 12px;")

        self.prev_button = QPushButton("⬅️ Previous")
        self.next_button = QPushButton("Next ➡️")
        self.prev_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.next_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)

        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(30)
        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        nav_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.position_label)
        layout.addStretch()
        layout.addLayout(nav_layout)
        layout.addSpacing(15)

        self.setLayout(layout)
        self.update_image()

    def update_image(self):
        if 0 <= self.current_index < len(self.image_paths):
            pixmap = QPixmap(self.image_paths[self.current_index])
            pixmap = pixmap.scaled(
                self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.label.setPixmap(pixmap)
            self.position_label.setText(
                f"Image {self.current_index + 1} of {len(self.image_paths)}"
            )

    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_image()

    def show_next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.update_image()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.show_previous_image()
        elif event.key() == Qt.Key_Right:
            self.show_next_image()
        else:
            super().keyPressEvent(event)
