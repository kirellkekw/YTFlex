"""
Utility function to create a download link for a file.
"""

from urllib.parse import quote
import os
import config


def create_download_link(filename: str):
    """
    Creates a download link for the file
    Args:
        filename: FULL filename of the file, including the extension
    """

    ip_or_domain = os.getenv("ip_or_domain", config.get("IP_OR_DOMAIN"))
    root_path = os.getenv("root_path", config.get("ROOT_PATH", "/ytflex"))

    return f"{ip_or_domain}/{root_path}/cdn/{quote(filename)}"
