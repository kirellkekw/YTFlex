"""
Utility function to check if a URL is valid.
"""

import requests


def is_valid_url(link: str) -> bool:
    """
    Checks if a URL is valid or not.

    Args:
        link: The URL to check.
    Returns:
        True if the URL is valid, False otherwise.
    """
    try:
        return requests.head(link, timeout=5).status_code == 200
    except requests.RequestException:
        return False
