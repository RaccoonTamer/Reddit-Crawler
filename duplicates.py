from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog,
    QScrollArea, QGridLayout, QProgressBar, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import os
from PIL import Image
import imagehash
from collections import defaultdict

class MoveThread(QThread):
    def __init__(self, files, target_folder):
        super().__init__()
        self.files = files
        self.target_folder = target_folder

    def run(self):
        for file in self.files:
            try:
                if os.path.exists(file):
                    file_name = os.path.basename(file)
                    target_path = os.path.join(self.target_folder, file_name)
                    if os.path.exists(target_path):
                        name, ext = os.path.splitext(file_name)
                        counter = 1
                        while os.path.exists(target_path):
                            target_path = os.path.join(self.target_folder, f"{name}_{counter}{ext}")
                            counter += 1
                    os.rename(file, target_path)
            except Exception as e:
                print(f"Failed to move {file}: {e}")

class DuplicatesThread(QThread):
    update_message = pyqtSignal(str)
    done_signal = pyqtSignal()
    progress_signal = pyqtSignal(int)
    add_duplicates_signal = pyqtSignal(dict)

    def __init__(self, folder_path, batch_size=50):
        super().__init__()
        self.folder_path = folder_path
        self.batch_size = batch_size

    def run(self):
        self.update_message.emit("🔍 Looking for duplicate images. . .")
        all_images = self.get_image_files()
        total_images = len(all_images)
        processed = 0
        hash_dict = defaultdict(list)

        for i in range(0, total_images, self.batch_size):
            batch = all_images[i:i + self.batch_size]
            for file in batch:
                image_hash = self.get_image_hash(file)
                if image_hash:
                    hash_dict[image_hash].append(file)
            processed += len(batch)
            self.progress_signal.emit(int((processed / total_images) * 100))

        duplicates = {h: files for h, files in hash_dict.items() if len(files) > 1}
        self.add_duplicates_signal.emit(duplicates)
        self.done_signal.emit()

    def get_image_files(self):
        return [
            os.path.join(root, file)
            for root, _, files in os.walk(self.folder_path)
            for file in files
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))
        ]

    def get_image_hash(self, path):
        try:
            img = Image.open(path)
            img = img.resize((256, 256))
            return str(imagehash.phash(img))
        except Exception as e:
            print(f"Hashing failed for {path}: {e}")
            return None


class DuplicatesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.folder_path = ""
        self.duplicate_groups = {}
        self.selected_files = []
        self.dot_count = 0
        self.is_dark_mode = True
        self.row = 0
        self.col = 0
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.header_label = QLabel("Duplicate Images")
        self.header_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #5aaaff;")
        self.layout.addWidget(self.header_label)

        self.feedback_label = QLabel("Select a folder to scan for duplicates")
        self.feedback_label.setStyleSheet("color: #bbb; font-size: 16px;")
        self.layout.addWidget(self.feedback_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet(""" 
            QProgressBar {
                border-radius: 10px;
                background-color: #2a2a2a;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #5aaaff;
                border-radius: 10px;
            }
        """)
        self.layout.addWidget(self.progress_bar)

        self.gallery_area = QScrollArea()
        self.gallery_widget = QWidget()
        self.gallery_layout = QGridLayout()
        self.gallery_layout.setSpacing(10)
        self.gallery_layout.setAlignment(Qt.AlignTop)
        self.gallery_widget.setLayout(self.gallery_layout)
        self.gallery_area.setWidget(self.gallery_widget)
        self.gallery_area.setWidgetResizable(True)
        self.layout.addWidget(self.gallery_area)

        button_layout = QHBoxLayout()
        self.delete_button = QPushButton("🗑️ Delete Selected")
        self.delete_button.setStyleSheet(self.button_style())
        self.delete_button.clicked.connect(self.delete_selected)

        self.move_button = QPushButton("📁 Move Selected")
        self.move_button.setStyleSheet(self.button_style())
        self.move_button.clicked.connect(self.move_selected)

        self.select_all_button = QPushButton("🔲 Select All")
        self.select_all_button.setStyleSheet(self.button_style())
        self.select_all_button.clicked.connect(self.select_all)

        self.unselect_all_button = QPushButton("❌ Unselect All")
        self.unselect_all_button.setStyleSheet(self.button_style())
        self.unselect_all_button.clicked.connect(self.unselect_all)

        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.move_button)
        button_layout.addWidget(self.select_all_button)
        button_layout.addWidget(self.unselect_all_button)
        self.layout.addLayout(button_layout)

        self.select_folder_button = QPushButton("Select Folder to Scan for Duplicates")
        self.select_folder_button.setStyleSheet(self.button_style())
        self.select_folder_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_folder_button)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_feedback_animation)

    def button_style(self):
        return """
            QPushButton {
                background-color: #5aaaff;
                color: white;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b8bff;
            }
        """

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            self.duplicate_groups = {}
            self.selected_files.clear()
            self.feedback_label.setText("<b>🔍 Looking for duplicate images. . .</b>")
            self.progress_bar.setValue(0)
            self.timer.start(500)
            self.start_duplicate_search()

    def start_duplicate_search(self):
        self.thread = DuplicatesThread(self.folder_path)
        self.thread.update_message.connect(self.update_feedback_label)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.done_signal.connect(self.on_search_done)
        self.thread.add_duplicates_signal.connect(self.on_duplicates_found)
        self.thread.start()

    def update_feedback_animation(self):
        self.dot_count = (self.dot_count + 1) % 4
        dots = '.' * self.dot_count
        self.feedback_label.setText(f"<b><font color='green'>🔍 Looking for duplicate images{dots}</font></b>")

    def update_feedback_label(self, message):
        self.feedback_label.setText(f"<b><font color='green'>{message}</font></b>")

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def on_search_done(self):
        self.timer.stop()
        self.feedback_label.setText("<b><font color='green'>🔍 Duplicate images found!</font></b>")

    def on_duplicates_found(self, duplicates):
        self.duplicate_groups = duplicates
        self.display_gallery()

    def display_gallery(self):
        for i in reversed(range(self.gallery_layout.count())):
            widget = self.gallery_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.row = 0
        self.col = 0

        for image_hash, file_list in self.duplicate_groups.items():
            remaining = [f for f in file_list if os.path.exists(f)]
            if len(remaining) < 2:
                continue
            self.duplicate_groups[image_hash] = remaining
            rep_path = remaining[0]
            self.display_single_image(rep_path, remaining)

    def display_single_image(self, path, file_list):
        try:
            label = QLabel()
            label.setCursor(Qt.PointingHandCursor)
            label.setFixedSize(220, 220)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(""" 
                QLabel {
                    background-color: #111;
                    border-radius: 12px;
                    padding: 5px;
                    border: 1px solid #333;
                }
                QLabel:hover {
                    border: 2px solid #5aaaff;
                    background-color: #222;
                }
            """)
            pixmap = QPixmap(path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            label.setProperty("file_path", path)
            label.mousePressEvent = self.make_image_click_handler(path, label)
            self.gallery_layout.addWidget(label, self.row, self.col)
            self.col += 1
            if self.col >= 4:
                self.col = 0
                self.row += 1
        except Exception as e:
            print("Error showing image:", e)

    def make_image_click_handler(self, path, label_widget):
        def handler(event):
            if path in self.selected_files:
                self.selected_files.remove(path)
                label_widget.setStyleSheet(""" 
                    QLabel {
                        background-color: #111;
                        border-radius: 12px;
                        padding: 5px;
                        border: 1px solid #333;
                    }
                """)
            else:
                self.selected_files.append(path)
                label_widget.setStyleSheet(""" 
                    QLabel {
                        background-color: #111;
                        border-radius: 12px;
                        padding: 5px;
                        border: 2px solid #00ff00;
                    }
                """)
        return handler

    def delete_selected(self):
        if not self.selected_files:
            QMessageBox.information(self, "No Selection", "❗ Nothing is selected.")
            return
        reply = QMessageBox.question(self, "Delete Files", "Are you sure you want to delete the selected files?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for file in self.selected_files:
                if os.path.exists(file):
                    os.remove(file)
            self.selected_files.clear()
            self.display_gallery()
            QMessageBox.information(self, "Deleted", "Selected files have been deleted.")

    def move_selected(self):
        if not self.selected_files:
            QMessageBox.information(self, "No Selection", "❗ Nothing is selected.")
            return
        target_folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if not target_folder:
            return
        self.thread = MoveThread(self.selected_files, target_folder)
        self.thread.start()
        self.thread.finished.connect(self.display_gallery)

    def select_all(self):
        self.selected_files = list(self.duplicate_groups.keys())
        self.display_gallery()

    def unselect_all(self):
        self.selected_files.clear()
        self.display_gallery()
