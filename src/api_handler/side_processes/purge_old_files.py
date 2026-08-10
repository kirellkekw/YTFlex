"""
Utility side process to purge old files from the download directory after a certain time.
"""

import asyncio
import logging
import time
from pathlib import Path

import config

logger = logging.getLogger("uvicorn.error")

DOWNLOAD_PATH = Path("./mountpoint/downloads")
CHECK_INTERVAL_SECONDS = 60


async def purge_old_files():
    """Purge files older than MAX_FILE_AGE (from config) from the download directory."""

    logger.info("File purge subprocess started.")
    DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)

    while True:
        try:
            max_file_age = config.get("MAX_FILE_AGE")
            _purge_once(max_file_age)
        except Exception:
            # Never let one bad iteration kill the background task permanently
            logger.exception("Error while purging old files")

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)


def _purge_once(max_file_age: float) -> None:
    now = time.time()

    for folder_path in DOWNLOAD_PATH.iterdir():
        if not folder_path.is_dir():
            continue

        for file_path in folder_path.iterdir():
            try:
                if not file_path.is_file():
                    continue

                file_age = now - file_path.stat().st_ctime
                if file_age > max_file_age:
                    logger.info("Deleting %s, %.0f seconds old", file_path, file_age)
                    file_path.unlink()
            except FileNotFoundError:
                # File was already removed concurrently (e.g. race with another
                # process/request) - safe to ignore
                continue
            except OSError:
                logger.exception("Failed to remove file %s", file_path)

        # Remove parent directory if now empty
        try:
            if not any(folder_path.iterdir()):
                folder_path.rmdir()
        except OSError:
            logger.exception("Failed to remove empty directory %s", folder_path)
