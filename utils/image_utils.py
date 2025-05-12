import os
from PIL import Image, UnidentifiedImageError
from imagehash import phash

def find_duplicates_by_pixel_hash(folder):
    image_hashes = {}
    duplicates = []

    for filename in os.listdir(folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(folder, filename)
            try:
                with Image.open(filepath) as img:
                    img_hash = phash(img)
                    if img_hash in image_hashes:
                        duplicates.append((image_hashes[img_hash], filepath))
                    else:
                        image_hashes[img_hash] = filepath
            except UnidentifiedImageError:
                print(f"Skipping invalid or corrupt image file: {filepath}")
                continue
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
                continue

    return duplicates

def find_duplicates_by_info_hash(folder):
    image_info = {}
    duplicates = []

    for filename in os.listdir(folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(folder, filename)
            try:
                with Image.open(filepath) as img:
                    img_info = (img.size, img.mode, img.info.get('dpi', None))
                    if img_info in image_info:
                        duplicates.append((image_info[img_info], filepath))
                    else:
                        image_info[img_info] = filepath
            except UnidentifiedImageError:
                print(f"Skipping invalid or corrupt image file: {filepath}")
                continue
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
                continue

    return duplicates
