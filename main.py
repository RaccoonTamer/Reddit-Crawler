import sys
import time
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTabWidget, QScrollArea, QGridLayout, QMessageBox,
    QComboBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import Qt
from threads import ImageDownloaderThread
from dialogs import ImagePreviewDialog
from duplicates import DuplicatesTab
from settings import SettingsTab

VERSION = "1.0.2"

def check_for_update(current_version):
    try:
        url = "https://raw.githubusercontent.com/RaccoonTamer/Reddit-Crawler/main/version.txt"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version != current_version:
                msg = QMessageBox()
                msg.setWindowTitle("🔔 Update Available")
                msg.setText(
                    f"A new version ({latest_version}) is available!\n"
                    f"You're using {current_version}.\n\n"
                    "Visit GitHub to download the latest version."
                )
                msg.setIcon(QMessageBox.Information)
                msg.setDetailedText("https://github.com/RaccoonTamer/Reddit-Crawler/releases")

                take_me_there_button = msg.addButton("Take Me There", QMessageBox.ActionRole)
                close_button = msg.addButton("Close", QMessageBox.RejectRole)

                msg.setStyleSheet("""
                    QMessageBox {
                        background-color: #2e2e2e;
                        color: white;
                    }
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px;
                        border-radius: 5px;
                    }
                    QPushButton:hover { background-color: #45a049; }
                """)

                button_clicked = msg.exec_()

                if msg.clickedButton() == take_me_there_button:
                    import webbrowser
                    webbrowser.open("https://github.com/RaccoonTamer/Reddit-Crawler/releases")
    except Exception as e:
        print("Update check failed:", e)

class RedditDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📥 Reddit Media Downloader")
        self.setGeometry(100, 100, 1000, 800)
        self.setFont(QFont("Segoe UI Emoji", 10))
        self.image_paths = []  
        self.last_results = []  
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #2e2e2e; }
            QLabel { color: white; }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #45a049; }
            QLineEdit {
                background-color: #444;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QTabWidget::pane { border: none; }
            QTabWidget::tab-bar { alignment: center; }
            QTabBar::tab {
                background-color: #444;
                color: white;
                padding: 10px;
                margin-right: 5px;
                border-radius: 3px;
            }
            QTabBar::tab:hover { background-color: #555; }
            QTabBar::tab:selected { background-color: #333; }
        """)

        self.tabs = QTabWidget()
        self.download_tab = QWidget()
        self.duplicates_tab = DuplicatesTab(self)
        self.settings_tab = SettingsTab(self)

        self.tabs.addTab(self.download_tab, "📥 Download")
        self.tabs.addTab(self.duplicates_tab, "🗑️ Duplicates")
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")

        self.init_download_tab()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def init_download_tab(self):
        layout = QVBoxLayout()

        header = QLabel("📥 Welcome to Reddit Image Fetcher")
        header.setFont(QFont("Segoe UI Emoji", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter) 
        layout.addWidget(header)

        form_layout = QHBoxLayout()
        self.subreddit_input = QLineEdit()
        self.subreddit_input.setPlaceholderText("Enter subreddit name")
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("Number of posts")
        start_button = QPushButton("⬇️ Start Download")
        start_button.clicked.connect(self.handle_download)

      
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Download Order", "Newest", "Oldest", "Highest Score"])
        self.sort_combo.setStyleSheet("""
            QComboBox {
                background-color: #555555;
                color: white;
                border: 1px solid #777;
                padding: 5px;
                border-radius: 5px;
                min-width: 130px;
            }
            QComboBox:hover {
                background-color: #666666;
            }
            QComboBox::drop-down {
                border-left: 1px solid #777;
            }
        """)
        self.sort_combo.currentIndexChanged.connect(self.sort_gallery_if_loaded)

        form_layout.addWidget(QLabel("📂 Subreddit:"))
        form_layout.addWidget(self.subreddit_input)
        form_layout.addWidget(QLabel("🔢 Posts:"))
        form_layout.addWidget(self.count_input)
        form_layout.addWidget(QLabel("🔽 Sort By:"))
        form_layout.addWidget(self.sort_combo)
        form_layout.addWidget(start_button)

        layout.addLayout(form_layout)

        self.loading_label = QLabel("")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("color: #5aaaff; font-weight: bold; padding: 8px;")
        layout.addWidget(self.loading_label)

        self.gallery_area = QScrollArea()
        self.gallery_widget = QWidget()
        self.gallery_layout = QGridLayout()
        self.gallery_layout.setSpacing(10)
        self.gallery_layout.setAlignment(Qt.AlignTop)
        self.gallery_widget.setLayout(self.gallery_layout)
        self.gallery_area.setWidget(self.gallery_widget)
        self.gallery_area.setWidgetResizable(True)

        layout.addWidget(QLabel("🖼️ Image Gallery"))
        layout.addWidget(self.gallery_area)

        self.download_tab.setLayout(layout)

    def handle_download(self):
        subreddit = self.subreddit_input.text().strip()
        try:
            count = int(self.count_input.text().strip())
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid number.")
            return

        if not subreddit:
            QMessageBox.critical(self, "Error", "Subreddit cannot be empty.")
            return

        self.loading_label.setText("🔍 Starting fetch...")
        self.loading_label.show()

        self.thread = ImageDownloaderThread(subreddit, count)
        self.thread.progress.connect(self.loading_label.setText)
        self.thread.images_downloaded.connect(self.on_images_downloaded)
        self.thread.finished.connect(self.on_download_finished)
        self.thread.start()

    def on_images_downloaded(self, results):
        self.last_results = results
        self.loading_label.hide()
        self.display_gallery(results)

    def on_download_finished(self):
        print("Download finished")
        self.thread = None

    def sort_gallery_if_loaded(self):
        if hasattr(self, 'last_results') and self.last_results:
            self.display_gallery(self.last_results)

    def display_gallery(self, results):
       
        sort_method = self.sort_combo.currentText()

        def get_sort_key(item):
           
            meta = item[1] if isinstance(item, tuple) else item
            if sort_method == "Newest":
                return -meta.get("created_utc", 0)
            elif sort_method == "Oldest":
                return meta.get("created_utc", 0)
            elif sort_method == "Highest Score":
                return -meta.get("score", 0)
            else: 
                return 0

        
        if sort_method != "Download Order":
            results = sorted(results, key=get_sort_key)

       
        for i in reversed(range(self.gallery_layout.count())):
            widget = self.gallery_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.row = 0
        self.col = 0
        self.columns = 3
        self.image_paths = []  

        for result in results:
            if isinstance(result, tuple):
                path, meta = result
            else:
                path = result.get("path")
                meta = result

            self.display_single_image(path, meta)

    def display_single_image(self, path, meta):
        try:
            container = QWidget()
            container_layout = QVBoxLayout()
            container_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            container.setLayout(container_layout)

            image_label = QLabel()
            image_label.setCursor(Qt.PointingHandCursor)
            image_label.setFixedSize(220, 220)
            image_label.setStyleSheet("""
                QLabel {
                    background-color: #111;
                    border-radius: 12px;
                    padding: 5px;
                    border: none;
                }
            """)
            pixmap = QPixmap(path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.mousePressEvent = self.make_image_click_handler(path, image_label)

          
            clean_permalink = meta.get("permalink", "").replace("https://reddit.com", "").replace("https//reddit.com", "")

            meta_label = QLabel(f"""
                <b>{meta.get('title', '')}</b><br>
                👤 {meta.get('author', '')} | ⬆️ {meta.get('score', 0)}<br>
                🕒 {time.strftime('%Y-%m-%d %H:%M', time.gmtime(meta.get('created_utc', 0)))}<br>
                <a href='https://reddit.com{clean_permalink}'>🔗 Open on Reddit</a>
            """)
            meta_label.setTextFormat(Qt.RichText)
            meta_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            meta_label.setOpenExternalLinks(True)
            meta_label.setWordWrap(True)
            meta_label.setStyleSheet("""
                color: white;
                font-size: 12px;
                padding: 10px;
                border-radius: 10px;
                background-color: rgba(60, 60, 60, 0.9);
                max-width: 220px;
                white-space: normal;
                min-height: 50px;
            """)

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QColor(0, 0, 0, 160))
            shadow.setOffset(0, 4)
            container.setGraphicsEffect(shadow)

            container.setStyleSheet("""
                QWidget:hover {
                    border: 2px solid #aaa;
                    border-radius: 15px;
                    background-color: #3c3c3c;
                }
            """)

            container_layout.addWidget(image_label, alignment=Qt.AlignCenter)
            container_layout.addWidget(meta_label, alignment=Qt.AlignCenter)
            self.gallery_layout.addWidget(container, self.row, self.col)

            self.image_paths.append(path) 

            self.col += 1
            if self.col >= self.columns:
                self.col = 0
                self.row += 1

        except Exception as e:
            print("Error showing image:", e)

    def make_image_click_handler(self, path, label):
        def handler(event):
            label.setStyleSheet(""" QLabel {
                background-color: #111;
                border-radius: 12px;
                padding: 5px;
                border: 2px solid blue;
            } """)
            try:
                index = self.image_paths.index(path)
            except ValueError:
                index = 0
            dialog = ImagePreviewDialog(self.image_paths, index, self)
            dialog.exec_()
        return handler

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RedditDownloaderApp()
    window.show()
    check_for_update(VERSION)
    sys.exit(app.exec_())
