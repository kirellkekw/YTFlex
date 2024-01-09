import asyncio
import os
import time
from config import *


async def purge_old_files():
    while True:
        await asyncio.sleep(60)  # every minute
        for file in os.listdir(download_directory):
            last_change = os.path.getmtime(
                os.path.join(download_directory, file))
            now = time.time()
            file_age = int(now - last_change)
            # print(file_age)
            if file_age > max_file_age:
                os.remove(os.path.join(download_directory, file))


async def main():
    await asyncio.gather(purge_old_files())

asyncio.run(main())
