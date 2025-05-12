import os
import time
import hashlib
import requests
from urllib.parse import urlparse

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif'}
VIDEO_EXTS = {'.mp4', '.gifv'}
SEEN_URLS_FILE = 'downloaded_urls.txt'

def is_valid_url(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=5)
        return r.status_code == 200 and 'content-type' in r.headers
    except requests.RequestException:
        return False

def has_been_downloaded(url):
    if not os.path.exists(SEEN_URLS_FILE):
        return False
    with open(SEEN_URLS_FILE, encoding='utf-8') as f:
        return url.strip() in f.read().splitlines()

def mark_as_downloaded(url):
    with open(SEEN_URLS_FILE, 'a', encoding='utf-8') as f:
        f.write(url.strip() + '\n')

def unique_filename(url, folder):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    h = hashlib.sha256(r.content).hexdigest()
    name, ext = os.path.splitext(os.path.basename(urlparse(url).path))
    ts = int(time.time())
    fname = f"{name}_{h}_{ts}{ext}"
    while os.path.exists(os.path.join(folder, fname)):
        ts += 1
        fname = f"{name}_{h}_{ts}{ext}"
    return fname, r.content

def download_image(url, folder):
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    if ext in VIDEO_EXTS or ext not in IMAGE_EXTS:
        return None
    if not is_valid_url(url) or has_been_downloaded(url):
        return None
    os.makedirs(folder, exist_ok=True)
    fname, content = unique_filename(url, folder)
    path = os.path.join(folder, fname)
    with open(path, 'wb') as f:
        f.write(content)
    mark_as_downloaded(url)
    return path

def fetch_subreddit_media_urls(subreddit, count, after=None, return_after=False):
    posts = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    next_after = after

    while len(posts) < count:
        api = f"https://www.reddit.com/r/{subreddit}/new/.json?limit=100"
        if next_after:
            api += f"&after={next_after}"

        try:
            response = requests.get(api, headers=headers, timeout=10)
            if response.status_code != 200:
                raise Exception(f"Reddit API error {response.status_code}: {response.text}")

            data = response.json()
            children = data.get('data', {}).get('children', [])

            for item in children:
                d = item['data']
                url = d.get('url_overridden_by_dest') or d.get('url')
                if url and any(url.lower().endswith(ext) for ext in IMAGE_EXTS):
                    if url not in [p['url'] for p in posts] and not has_been_downloaded(url):
                        posts.append({
                            'url': url,
                            'title': d.get('title', ''),
                            'author': d.get('author', ''),
                            'score': d.get('score', 0),
                            'created_utc': d.get('created_utc', 0),
                            'permalink': f"https://reddit.com{d.get('permalink', '')}"
                        })

            next_after = data['data'].get('after')
            if not next_after:
                break

        except Exception as e:
            print(f"Error fetching posts: {e}")
            break

    if return_after:
        return posts[:count], next_after
    return posts[:count]
