# Utility functions for file operations
import os
import shutil
from mimetypes import guess_type

def get_file_type(file_path):
    mime_type, _ = guess_type(file_path)
    if mime_type:
        if mime_type.startswith('image'):
            return 'Images'
        elif mime_type.startswith('video'):
            return 'Videos'
        elif mime_type.startswith('audio'):
            return 'Audio'
        elif mime_type.startswith('application/pdf') or mime_type.startswith('text'):
            return 'Documents'
    return 'Others'

def move_file(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(src, dest)
