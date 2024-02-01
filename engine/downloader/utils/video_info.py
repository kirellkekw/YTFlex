"""
Utility class to store video information.
"""

from dataclasses import dataclass


@dataclass
class VideoInfo:
    """Data class to store video information."""

    def __init__(self, title: str, duration: int, url: str, thumbnail: str):
        self.url = url
        self.title = title
        self.duration = duration
        self.thumbnail = thumbnail
