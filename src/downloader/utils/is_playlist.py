"""
Utility function for checking if a URL is a playlist.
"""


def is_playlist(link: str) -> bool:
    """Checks if a URL is a playlist or not"""

    if len(link) == 34 and "playlist?list=" not in link and "watch?v=" not in link:
        # probably a playlist id since it's 34 characters long
        return True

    return "playlist?list=" in link
