"""
Utility side process to purge old files from the download directory after a certain time.
"""

import asyncio
import os
import time
from config import DOWNLOAD_PATH, MAX_FILE_AGE


async def purge_old_files():
    """Purge files older than max_file_age defined in config.py from download_directory"""
    print("File purge subprocess started.")  # debug
    while True:
        await asyncio.sleep(60)  # check every minute
        for file in os.listdir(DOWNLOAD_PATH):
            # get creation time of file
            last_change = os.path.getctime(
                os.path.join(DOWNLOAD_PATH, file))
            now = time.time()
            file_age = int(now - last_change)
            # print(file, file_age)
            if file_age > MAX_FILE_AGE:
                print(f"Deleting {file}, {file_age} seconds old")
                os.remove(os.path.join(DOWNLOAD_PATH, file))
