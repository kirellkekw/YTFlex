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
    if len(link) == 11:
        # probably a video id, check if the link is alive
        return (
            requests.head(
                f"https://www.youtube.com/watch?v={link}", timeout=5
            ).status_code
            == 200
        )

    return requests.head(link, timeout=5).status_code == 200
