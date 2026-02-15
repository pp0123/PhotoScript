import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import shutil
from tqdm import tqdm


def get_exif_date(path):
    try:
        with Image.open(path) as image:  # 'with' ensures the file is closed properly
            info = image._getexif()
            if info:
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded == "DateTimeOriginal":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return datetime.fromtimestamp(os.path.getmtime(path))


def organize_photos():
    source_dir = os.getcwd()
    extensions = (".jpg", ".jpeg", ".png", ".heic")

    # Gather all image files first so we know how many there are
    files_to_move = [
        f for f in os.listdir(source_dir) if f.lower().endswith(extensions)
    ]

    if not files_to_move:
        print("No photos found to organize!")
        return

    print(f"Organizing {len(files_to_move)} photos...")

    # Wrap the list in 'tqdm' to create the progress bar
    for filename in tqdm(files_to_move, desc="Processing Photos", unit="img"):
        file_path = os.path.join(source_dir, filename)
        date = get_exif_date(file_path)

        new_path = os.path.join(
            "Photos", date.strftime("%Y"), date.strftime("%m"), date.strftime("%d")
        )

        os.makedirs(new_path, exist_ok=True)
        new_filename = f"{date.strftime('%Y%m%d')}_{filename}"
        final_destination = os.path.join(new_path, new_filename)

        shutil.move(file_path, final_destination)


if __name__ == "__main__":
    organize_photos()
    print("All photos organized successfully!")
