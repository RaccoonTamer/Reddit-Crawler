Discord: dookie#7175

Reddit Media Downloader 📥
Want to grab images from Reddit without the hassle? This app makes it easy! You can pick a subreddit, set how many posts you want to pull, and let the app do the rest. It’ll download the images you want and even keep things tidy by making sure you don’t get any duplicates. Plus, it tracks useful details for each image, like the post title, author, upvotes, and when it was uploaded.


![Cats](https://github.com/user-attachments/assets/d9036471-edf5-4466-8dac-30f1bc5b072f)


✅ What It Does:
Metadata at a Glance 📝
Each image comes with key info like the title, author, upvotes, and posting time.

No Duplicates 🚫
It remembers which images you've already downloaded, so you won’t get the same ones twice.

Fetches New Content 🔄
The app pulls in the latest media from a subreddit, using smart requests to avoid hitting Reddit’s API limits. It keeps everything running smoothly, even when you’re pulling a lot of posts.

Easy-to-Use Interface 🖥️
The simple, clean layout makes navigating a breeze. You can input the subreddit name, choose the number of posts you want, and then see everything in a gallery view to easily browse the images.

NSFW Content 🔥
This app also lets you download NSFW images by bypassing Reddit's usual filters, so you can access and save content marked as explicit without any issues.

Videos Coming Soon 🎥
Right now, the app only handles images, but video downloads are on the way in the next update. Stay tuned!

Whether you’re a Reddit fan, a curator, or just want to archive cool images from the site (including NSFW), this app is a perfect solution. Forget about manually saving images one by one—let the app take care of it! 🙌

🛠️ How to Use
Install Python
1. Make sure you have Python 3.10 or higher installed on your system. You can download it from:
https://www.python.org/downloads/

2. Clone or Download the Repository

Clone via Git:

git clone https://github.com/RaccoonTamer/Reddit-Crawler.git
cd Reddit-Crawler
Or download the ZIP from GitHub and extract it.

Install Dependencies
Make sure you're in the project folder, then run:

pip install -r requirements.txt
Run the App
Start the program with:

python main.py
Enter a Subreddit and Number of Posts
In the GUI, type the name of a subreddit (e.g. cats, nature, NSFW) and specify how many posts you want to fetch.

Download and View
Click Download, and the app will automatically fetch and save the images along with metadata.

⚠️ Known Bugs:
Broken Reddit Post Links
Clicking on Reddit URLs in the metadata section currently opens malformed links like reddit.comhttps, resulting in an error:
“This site can’t be reached. reddit.comhttps’s server IP address could not be found.”

Images Sometimes Don’t Appear
Some posts show empty previews or missing thumbnails even though the image has been downloaded. This could be due to:

Reddit hosting issues (e.g. removed or deleted content)

Certain file formats not being supported in the preview,

📄 License and Disclaimer:
This project is open-source under the specified license (see LICENSE.txt). Feel free to use, modify, and distribute it. This tool is intended for educational and personal use only. Please respect Reddit's Terms of Service.

🙏 Attribution:
If you use or feature this project in your own work, please provide proper credit by linking back to the GitHub repo:
🔗 https://github.com/RaccoonTamer/Reddit-Crawler
