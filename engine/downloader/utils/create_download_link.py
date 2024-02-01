"""
Utility function to create a download link for a file.
"""

from urllib.parse import quote
from config import IP_OR_DOMAIN


def create_download_link(filename: str):
    """
    Creates a download link for the file
    Args:
        filename: FULL filename of the file, including the extension
    """
    return f"http://{IP_OR_DOMAIN}/cdn/{quote(filename)}"
