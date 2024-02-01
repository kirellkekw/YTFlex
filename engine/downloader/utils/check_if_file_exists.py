"""
Utility function to check if a file exists in the download directory.
"""

import os
from config import DOWNLOAD_PATH


def check_if_file_exists(file_address: str):
    """
    Checks if the file exists in the download directory.

    Args:
        file_address (str): The address of the file to check.

    Returns:
        str: The filename if the file exists, "" if it doesn't.
    """
    # not the most efficient way, but it works
    for file in os.listdir(DOWNLOAD_PATH):
        # check if the file exists without the extension
        if file.startswith(file_address + "."):
            print(f"File already exists, name: {file}")
            return file
    return ""
