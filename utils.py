import os
from pathlib import Path
STATIC_DIR = Path('static')
PHOTOS_DIR = STATIC_DIR / 'fotos'
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
def save_uploaded_photo(temp_path, filename):
    dest = PHOTOS_DIR / filename
    # if temp_path is path on another FS, use copy
    import shutil
    shutil.copy(temp_path, dest)
    return str(dest)
