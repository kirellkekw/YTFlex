"""
Utility function to check if a URL is valid.
"""

import re
from urllib.parse import urlparse, parse_qs, unquote


def parse_video_id(link: str) -> str | bool:
    """
    Checks if a URL is valid or not, and parses video IDs as well.

    Args:
        link: The URL to check.
    Returns:
        The video ID if parsable, False otherwise.
    """

    quick_parsable = [
        "/watch/",
        "/v/",
        "/embed/",
        "/shorts/",
        "/live/",
        "/e/",
    ]

    # Ensure a scheme so urlparse populates netloc/path correctly
    if not re.match(r"^\w+://", link):
        link = "https://" + link

    parsable = urlparse(link)
    video_id = None

    if parsable.path == "/watch":
        video_id = parse_qs(parsable.query).get("v", [None])[0]
    elif parsable.path == "/oembed":
        inner_link = parse_qs(parsable.query).get("url", [None])
        video_id = parse_video_id(unquote(inner_link[0])) if inner_link[0] else None
    elif parsable.path.startswith("/attribution_link"):
        u = parse_qs(parsable.query).get("u", [None])[0]
        if u:
            partial_link = unquote(u)
            video_id = parse_video_id(f"https://youtube.com{partial_link}")
    elif parsable.path.startswith("/"):
        parts = parsable.path.split("/")
        if len(parts) > 1 and parts[1]:
            video_id = parts[1][:11]

    for prefix in quick_parsable:
        if parsable.path.startswith(prefix):
            video_id = parsable.path.split(prefix)[1][:11]

    if video_id and len(video_id) == 11:
        return video_id

    return False  # catch-all failure case


if __name__ == "__main__":
    with open("test_links.txt", "r", encoding="utf-8") as f:
        for line in f:
            assert len(parse_video_id(line.strip())) == 11

        print("passing")
