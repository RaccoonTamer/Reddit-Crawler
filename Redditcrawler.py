import os
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import re
import time
import requests
from colorama import init, Fore
from urllib.parse import urlparse
import hashlib
import mimetypes
import shutil
from PIL import Image
import imagehash
import colorama
import concurrent.futures

init(autoreset=True)

def print_ascii_art():
    additional_art = """
     _  .-')     ('-.  _ .-') _  _ .-') _            .-') _                    _  .-')     ('-.      (`\ .-') /`            ('-.  _  .-')   
( \( -O )  _(  OO)( (  OO) )( (  OO) )          (  OO) )                  ( \( -O )   ( OO ).-.   `.( OO ),'          _(  OO)( \( -O )  
 ,------. (,------.\     .'_ \     .'_   ,-.-') /     '._          .-----. ,------.   / . --. /,--./  .--.  ,--.     (,------.,------.  
 |   /`. ' |  .---',`'--..._),`'--..._)  |  |OO)|'--...__)        '  .--./ |   /`. '  | \-.  \ |      |  |  |  |.-')  |  .---'|   /`. ' 
 |  /  | | |  |    |  |  \  '|  |  \  '  |  |  \'--.  .--'        |  |('-. |  /  | |.-'-'  |  ||  |   |  |, |  | OO ) |  |    |  /  | | 
 |  |_.' |(|  '--. |  |   ' ||  |   ' |  |  |(_/   |  |          /_) |OO  )|  |_.' | \| |_.'  ||  |.'.|  |_)|  |`-' |(|  '--. |  |_.' | 
 |  .  '.' |  .--' |  |   / :|  |   / : ,|  |_.'   |  |          ||  |`-'| |  .  '.'  |  .-.  ||         | (|  '---.' |  .--' |  .  '.' 
 |  |\  \  |  `---.|  '--'  /|  '--'  /(_|  |      |  |         (_'  '--'\ |  |\  \   |  | |  ||   ,'.   |  |      |  |  `---.|  |\  \  
 `--' '--' `------'`-------' `-------'   `--'      `--'            `-----' `--' '--'  `--' `--''--'   '--'  `------'  `------'`--' '--' 
    
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@@           @@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@,              @@@@@@@    @@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@@   @@@@@@@@@   @@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@(   @@@@@@@    @@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@@@@@           @@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&                .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@*             .#@@@@&/              @@@@@@@@@@@@@@@@@@@@@@
@@@@@         @@@       *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       #@@@         @@@@
@@     @@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      (@@@@@     @
@   @@@@@@(    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,    @@@@@@@   
}&   @@@@    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@   
@   @@@   @@@@@@@@@@@@@@///////@@@@@@@@@@@@@@@@///////&@@@@@@@@@@@@@    @@@   
@@       @@@@@@@@@@@@@@/////////@@@@@@@@@@@@@@/////////@@@@@@@@@@@@@@@
@@@@    @@@@@@@@@@@@@@@/////////@@@@@@@@@@@@@@/////////@@@@@@@@@@@@@@@
@@@@@   @@@@@@@@@@@@@@@@///////@@@@@@@@@@@@@@@@//////@@@@@@@@@@@@@@@@@
@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@
@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@
@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@
@@@@@@@    @@@@@@@@@@@@@@@@#  @@@@@@@@@@@@@@@@@@@@@  @@@@@@@@@@@@@@@@    @@@@@@@
@@@@@@@@@    @@@@@@@@@@@@@@@       @@@@@@@@@@@       @@@@@@@@@@@@@@     @@@@@@@@
@@@@@@@@@@@@     @@@@@@@@@@@@@@@                 @@@@@@@@@@@@@@@     @@@@@@@@@@@
{@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&      @@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@                                       @@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@    @@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@    @@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@   @@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@    @@@@@@@@@@@@@@
@@@@@@@@@@@@@@   @@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@   @@@@@@@@@@@@@@
@@@@@@@@@@@@@@   @@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@   @@@@@@@@@@@@@
@@@@@@@@@@@@@@   @@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@   @@@@@@@@@@@@@
@@@@@@@@@@@@@@   @@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@    @@@@@@@@@@@@@
@@@@@@@@@@@@@@@   @@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@@@   @@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@   @@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@@    @@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@    @@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@   @@     @@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@       @@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@     @@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@             @@@@@@@@@@@@@@@@@@              @@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@    @@@@@@@@@    @@@@@@@@@@@@@@@   @@@@@@@@@    @@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@   @@@@@@@@@@@@     @@@@@@@@@     @@@@@@@@@@@@   @@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@                                                 @@@@@@@@@@@@@@@
"""

    colorama.init(convert=True) 
    os.system("cls" if os.name == "nt" else "clear")

    rainbow_colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    colored_ascii_art = ""
    color_index = 0

    for line in additional_art.split('\n'):
        for char in line:
            if char != '\n':
                colored_ascii_art += rainbow_colors[color_index % len(rainbow_colors)] + char
                color_index += 1
            else:
                colored_ascii_art += char
        colored_ascii_art += '\n'
    combined_art = colored_ascii_art

    print(combined_art, end="")

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
VIDEO_EXTENSIONS = {'.mp4', '.gifv'}

def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200 and 'content-type' in response.headers
    except requests.exceptions.RequestException:
        return False

def get_file_extension(url):
    parsed_url = urlparse(url)
    _, file_extension = os.path.splitext(parsed_url.path)
    return file_extension.lower()

def get_unique_filename(url, folder):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_content_hash = hashlib.sha256(response.content).hexdigest()
        filename = os.path.basename(urlparse(url).path)
        base_name, extension = os.path.splitext(filename)
        timestamp = int(time.time())
        unique_filename = f"{base_name}_{image_content_hash}_{timestamp}{extension}"
        count = 1
        while os.path.exists(os.path.join(folder, unique_filename)):
            unique_filename = f"{base_name}_{image_content_hash}_{timestamp}_{count}{extension}"
            count += 1
        return unique_filename
    except requests.exceptions.MissingSchema:
        print(Fore.RED + "Invalid URL. Please provide a valid link starting with 'http://' or 'https://'")
        return None
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching the image: {e}")
        return None

def download_image(url, folder):
    if not is_valid_url(url):
        print(Fore.RED + f"Invalid URL: {url}")
        return

    file_extension = get_file_extension(url)

    if file_extension not in IMAGE_EXTENSIONS and file_extension not in VIDEO_EXTENSIONS:
        print(Fore.RED + f"Unsupported file format for URL: {url}")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()

        filename = get_unique_filename(url, folder)

        if file_extension in VIDEO_EXTENSIONS:
            print(Fore.YELLOW + f"Skipping {url} - GIFV files are not supported.")
            return

        with open(os.path.join(folder, filename), 'wb') as f:
            f.write(response.content)

        print(Fore.GREEN + f"{file_extension.capitalize()} downloaded successfully and saved as {filename}")

        if file_extension == '.gif':
            gif_folder = os.path.join(folder, 'Gifs')
            os.makedirs(gif_folder, exist_ok=True)
            new_file_path = os.path.join(gif_folder, filename)
            os.rename(os.path.join(folder, filename), new_file_path)
            print(Fore.GREEN + f"Moved GIF to 'Gifs' folder: {new_file_path}")

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error downloading the image: {e}")

def download_images_concurrently(image_urls, folder):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_image, url, folder) for url in image_urls]

        for future in concurrent.futures.as_completed(futures):
            future.result()

def read_downloaded_urls():
    try:
        with open("downloaded_urls.txt", "r") as f:
            downloaded_urls = f.read().splitlines()
            return downloaded_urls
    except FileNotFoundError:
        return []

def append_to_downloaded_urls(url):
    with open("downloaded_urls.txt", "a") as f:
        f.write(url + "\n")

before_value = None
downloaded_urls = set()

def fetch_image_urls_from_subreddit(subreddit, num_links):
    # Initialize the lists and variables
    image_urls = []
    after = None
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    while len(image_urls) < num_links:
        if after:
            url = f"https://www.reddit.com/r/{subreddit}/new/.json?limit=100&after={after}"
        else:
            url = f"https://www.reddit.com/r/{subreddit}/new/.json?limit=100"
            
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Extract image URLs from the current batch of data
        current_image_urls = [post['data']['url'] for post in data['data']['children']]
        image_urls.extend(current_image_urls)
        
        # Update the 'after' token for the next batch
        after = data['data']['after']
        
        # If there's no 'after' token, we've reached the end of the posts
        if not after:
            break

    return image_urls[:num_links]


def main_fetch_urls():
    global downloaded_urls

    print(Fore.BLUE + "Enter the name of the subreddit:")
    subreddit = input()

    print(Fore.BLUE + "Enter the number of links to fetch:")
    num_links = int(input())

    print(Fore.YELLOW + f"Fetching {num_links} image URLs from the subreddit '{subreddit}'...")

    image_urls = fetch_image_urls_from_subreddit(subreddit, num_links)

    with open("image_urls.txt", "a") as f:
        for url in image_urls:
            f.write(url + "\n")
        downloaded_urls.update(image_urls)

    print(Fore.GREEN + "Image URLs fetched and saved to image_urls.txt!")

def delete_non_images(directory):
    if not os.path.exists(directory):
        print("Directory not found.")
        return

    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    count_deleted = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if root == directory and not is_image_file(file_path):
                try:
                    os.remove(file_path)
                    count_deleted += 1
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    print(f"Total non-image files deleted: {count_deleted}")

def is_image_file(filename):
    return os.path.splitext(filename)[1].lower() in IMAGE_EXTENSIONS

def delete_duplicates(directory):
    if not os.path.exists(directory):
        print("Directory not found.")
        return

    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    image_hashes = {}
    count_deleted = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image_file(file_path):
                with Image.open(file_path) as img:
                    img_hash = imagehash.average_hash(img)
                if img_hash in image_hashes:
                    try:
                        os.remove(file_path)
                        count_deleted += 1
                        print(f"Deleted duplicate: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                else:
                    image_hashes[img_hash] = file_path

    print(f"Total duplicate files deleted: {count_deleted}")

def rename_files_in_folder(directory, pattern):
    if not os.path.exists(directory):
        print("Directory not found.")
        return

    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    image_files = [f for f in os.listdir(directory) if is_image_file(os.path.join(directory, f))]
    num_images = len(image_files)

    if num_images == 0:
        print("No image files found in the directory.")
        return

    if pattern == "1-100":
        for count, filename in enumerate(image_files, start=1):
            file_extension = os.path.splitext(os.path.join(directory, filename))[1]
            new_filename = f"{count}{file_extension}"
            new_file_path = os.path.join(directory, new_filename)
            os.rename(os.path.join(directory, filename), new_file_path)
    elif pattern == "a-z":
        for count, filename in enumerate(image_files, start=1):
            file_extension = os.path.splitext(os.path.join(directory, filename))[1]
            new_filename = f"{chr(ord('a') + (count - 1))}{file_extension}"
            new_file_path = os.path.join(directory, new_filename)
            os.rename(os.path.join(directory, filename), new_file_path)
    else:
        pattern_parts = pattern.split("-")
        if len(pattern_parts) == 2 and pattern_parts[0].isdigit() and pattern_parts[1].isdigit():
            start_number = int(pattern_parts[0])
            end_number = int(pattern_parts[1])
            if start_number <= end_number:
                for count, filename in enumerate(image_files, start=start_number):
                    if count > end_number:
                        print(f"Pattern exceeded. Stopping renaming process.")
                        break
                    file_extension = os.path.splitext(os.path.join(directory, filename))[1]
                    new_filename = f"{count}{file_extension}"
                    new_file_path = os.path.join(directory, new_filename)
                    os.rename(os.path.join(directory, filename), new_file_path)
            else:
                print("Invalid pattern: The start number should be less than or equal to the end number.")
        else:
            print("Invalid pattern format. Supported patterns are '1-100', 'a-z', or custom patterns like '1-10', 'a-d', etc.")

    print("Renaming complete.")

def count_image_urls():
    try:
        with open("image_urls.txt", "r") as f:
            image_urls = f.read().splitlines()
            num_images = len(image_urls)
            return num_images
    except FileNotFoundError:
        return 0

def option_1():
    print(Fore.BLUE + "Enter the directory path:")
    directory_path = input()
    delete_non_images(directory_path)

def option_2():
    print(Fore.BLUE + "Enter the directory path:")
    directory_path = input()
    delete_duplicates(directory_path)

def option_3():
    main_fetch_urls()

def option_4():
    try:
        print(Fore.BLUE + "Enter the name of the folder to save images:")
        folder_name = input()
        os.makedirs(folder_name, exist_ok=True)

        num_images_to_download = count_image_urls()
        print(Fore.YELLOW + f"Total number of images to download: {num_images_to_download}")

        confirm = input(Fore.YELLOW + "Do you want to proceed with the download? (y/n): ").lower()
        if confirm == 'n':
            num_images_to_download = int(input(Fore.YELLOW + f"How many images would you like to download "
                                                 f"(out of {num_images_to_download})? "))

        with open("image_urls.txt", "r") as f:
            image_urls = f.read().splitlines()

            for i in range(num_images_to_download):
                url = image_urls[i]
                print(Fore.YELLOW + f"Attempting to download URL {i + 1}/{num_images_to_download}: {url}")
                download_image(url, folder_name)
                append_to_downloaded_urls(url)

    except FileNotFoundError:
        print(Fore.RED + "Error: image_urls.txt not found. Please run option 3 first.")

def option_5():
    print(Fore.BLUE + "Enter the directory path:")
    directory_path = input()
    print(Fore.YELLOW + "Enter the renaming pattern (e.g., '1-100', 'a-z', 'a-d', etc.):")
    pattern = input()
    rename_files_in_folder(directory_path, pattern)

def main():
    init(autoreset=True)

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print_ascii_art()

        print(Fore.YELLOW + "\nSelect an option:")
        print(f"{Fore.CYAN}1. {Fore.MAGENTA}Delete non-image files")
        print(f"{Fore.CYAN}2. {Fore.MAGENTA}Delete duplicate photos")
        print(f"{Fore.CYAN}3. {Fore.MAGENTA}Fetch subreddit image URLs and save to image_urls.txt")
        print(f"{Fore.CYAN}4. {Fore.MAGENTA}Download images from saved image URLs in image_urls.txt")
        print(f"{Fore.CYAN}5. {Fore.MAGENTA}Rename image files in a specific directory")
        print(f"{Fore.CYAN}6. {Fore.MAGENTA}Exit")

        try:
            choice = int(input(Fore.YELLOW + "My option is: "))
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number from 1 to 6.")
            continue

        if choice == 1:
            option_1()
        elif choice == 2:
            option_2()
        elif choice == 3:
            option_3()
        elif choice == 4:
            option_4()
        elif choice == 5:
            option_5()
        elif choice == 6:
            print(Fore.YELLOW + "Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid option. Please select a valid option.")

if __name__ == "__main__":
    main()
