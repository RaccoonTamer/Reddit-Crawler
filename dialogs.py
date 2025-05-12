from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

class ImagePreviewDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🖼️ Image Preview")
        layout = QVBoxLayout(self)
        label = QLabel()
        pixmap = QPixmap(image_path)
        
        screen_size = QApplication.desktop().screenGeometry()
        max_width = screen_size.width() * 0.8
        max_height = screen_size.height() * 0.8
        
        pixmap = pixmap.scaled(int(max_width), int(max_height), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
