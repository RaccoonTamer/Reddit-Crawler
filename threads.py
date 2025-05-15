from PyQt5.QtCore import QThread, pyqtSignal
from utils import fetch_subreddit_media_urls, download_image
import os
import time
import json


class ImageDownloaderThread(QThread):
    images_downloaded = pyqtSignal(list)
    progress = pyqtSignal(str)

    def __init__(self, subreddit, count, parent=None):
        super().__init__(parent)
        self.subreddit = subreddit
        self.count = count

    def run(self):
        folder = os.path.join(os.getcwd(), self.subreddit)
        os.makedirs(folder, exist_ok=True)

        
        downloaded_file = "downloaded_urls.txt"
        if os.path.exists(downloaded_file):
            with open(downloaded_file, 'r') as f:
                downloaded_urls = set(line.strip() for line in f)
        else:
            downloaded_urls = set()

       
        cache_file = f"{self.subreddit}_cache.json"
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
                posts = cache_data.get("posts", [])
                current_index = cache_data.get("index", 0)
                after = cache_data.get("after", None)
        else:
            self.progress.emit(f"🔄 First-time fetch for u/{self.subreddit}, pulling initial 100 posts...")
            posts, after = fetch_subreddit_media_urls(self.subreddit, 100, after=None, return_after=True)
            current_index = 0

        results = []
        total_downloaded = 0

        while total_downloaded < self.count:
            if current_index >= len(posts):
                self.progress.emit(f"🔁 All cached posts processed. Fetching next 100 posts from u/{self.subreddit}...")
                try:
                    new_posts, after = fetch_subreddit_media_urls(self.subreddit, 100, after=after, return_after=True)
                    if not new_posts:
                        self.progress.emit("🚫 No more posts to fetch.")
                        break
                    posts.extend(new_posts)  
                    current_index = len(posts) - len(new_posts)
                except Exception as e:
                    self.progress.emit(f"❌ Error fetching more posts: {str(e)}")
                    break

            if current_index >= len(posts):
                break

            post = posts[current_index]
            current_index += 1

            url = post.get("url")
            if not url:
                self.progress.emit("⚠️ Skipping post with missing URL.")
                continue

            if url in downloaded_urls:
                self.progress.emit(f"⚠️ Already downloaded: {url}")
                continue

            if not self.is_valid_image(url):
                self.progress.emit(f"⚠️ Not an image file, skipping: {url}")
                continue

            self.progress.emit(f"⬇️ Downloading {total_downloaded + 1} of {self.count} from u/{self.subreddit}...")

            try:
                path = download_image(url, folder)
                if path:
                    metadata = {
                        "title": post.get("title", "No Title"),
                        "author": post.get("author", "Unknown"),
                        "score": post.get("score", 0),
                        "created_utc": post.get("created_utc", 0),
                        "permalink": f"https://reddit.com{post.get('permalink', '')}"
                    }
                    results.append((path, metadata))
                    total_downloaded += 1
                    with open(downloaded_file, 'a') as f:
                        f.write(url + '\n')
                    downloaded_urls.add(url)
                else:
                    self.progress.emit(f"⚠️ Download returned no file: {url}")
            except Exception as e:
                self.progress.emit(f"❌ Error downloading: {str(e)}")

            time.sleep(1.2)

        
        cache_data = {
            "posts": posts,
            "index": current_index,
            "after": after
        }
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)

        self.progress.emit(f"✅ Downloaded {total_downloaded} images.")
        self.images_downloaded.emit(results)

    def is_valid_image(self, url):
        valid_extensions = ('.jpg', '.jpeg', '.png')
        return url.lower().endswith(valid_extensions)
