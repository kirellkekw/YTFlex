"""
Utility function to create a response object for the client.
"""

import os


def create_response(
    cdn_link: str,
    thumbnail: str,
    filename: str,
    duration: int,
    already_downloaded: bool,
):
    """
    Creates and returns a response object for the client.

    Args:
        resolution: the resolution of the file, if it's audio, it'll be None
        link: the download link of the file
        title: the title of the file
        thumbnail: the thumbnail of the file
        duration: the duration of the file
        filename: the filename of the file
        already_downloaded: whether the file was already downloaded or not
    """

    if already_downloaded:
        message = "File is already downloaded"
    else:
        message = "File has been downloaded successfully"

    response = [
        {
            "link": cdn_link,
            "message": message,
            "metadata": {
                "title": filename.split(".")[0],
                "duration": duration,
                "thumbnail": thumbnail,
                "already_downloaded": already_downloaded,
                "filename": filename,
                "extension": os.path.splitext(filename)[1],
            },
        }
    ]

    return response


def create_error_response(message: str) -> dict:
    """
    Creates a response with error message.

    Args:
        error: The error message.

    Returns:
        A dictionary containing the error message.
    """

    # responses = {
    #     "invalidurl": "Invalid URL/ID provided",
    #     "unavailable": "Video is not accessible in our server location",
    #     "file_too_big": "Video is too big to download",
    #     "resolution_unavailable": "Requested resolution is not available for the video",
    #     "invalid_resolution": "Invalid resolution provided",
    # }
    # this will be put to use in the following commit(s), pinky promise

    return {"message": message}
