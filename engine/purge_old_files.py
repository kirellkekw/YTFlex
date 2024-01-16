import asyncio
import os
import time
from config import download_path, max_file_age


async def purge_old_files():
    """Purge files older than max_file_age defined in config.py from download_directory"""
    print("File purge subprocess started.")
    while True:
        await asyncio.sleep(60)  # every minute
        for file in os.listdir(download_path):
            # get creation time of file
            last_change = os.path.getctime(
                os.path.join(download_path, file))
            now = time.time()
            file_age = int(now - last_change)
            # print(file, file_age)
            if file_age > max_file_age:
                print(f"Deleting {file}, {file_age} seconds old")
                os.remove(os.path.join(download_path, file))
