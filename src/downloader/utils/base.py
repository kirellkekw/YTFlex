"""
This module is used as an easy export point for all the utility functions.
"""

from src.downloader.utils.create_download_link import create_download_link
from src.downloader.utils.create_response import (
    create_response,
    create_error_response,
)
from src.downloader.utils.extract_metadata import extract_info
from src.downloader.utils.filename_collector import FilenameCollectorPP
from src.downloader.utils.ydl_opts_builder import ydl_opts_builder
from src.downloader.utils.format_title import format_title
from src.downloader.utils.is_playlist import is_playlist
from src.downloader.utils.is_valid_url import is_valid_url
from src.downloader.utils.extract_playlist_metadata import parse_playlist

# from engine.downloader.utils.check_if_file_exists import check_if_file_exists

__all__ = [
    "create_download_link",
    #     "check_if_file_exists",
    "create_response",
    "create_error_response",
    "extract_info",
    "FilenameCollectorPP",
    "ydl_opts_builder",
    "format_title",
    "is_playlist",
    "is_valid_url",
    "parse_playlist",
]
