"""
Utility function for checking if a URL is a playlist.
"""


def is_playlist(link: str) -> bool:
    """Checks if a URL is a playlist or not"""
    return "playlist?list=" in link
