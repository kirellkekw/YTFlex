"""
Utility to find the appropriate resolution to download.
"""

import config


def find_appropriate_res(preferred_res: int | str):
    """
    Returns the nearest resolution that is lower than the preferred resolution defined in config.py.

    Also attempts to convert the passed resolution to an integer if it is a string.

    Args:
        preferred_res: The preferred resolution to download.
    """

    res_list: list[int] = config.get("RES_LIST")

    if preferred_res == str:
        # someone might have accidentally passed with p at the end
        # being the good dev we are, we'll just remove it
        preferred_res = preferred_res.replace("p", "")
        try:
            preferred_res = int(preferred_res)  # convert to int
        except ValueError:
            # i sincerely hope you know how resolutions and integers work if you're reading this
            print("Resolution must be an integer")
            return 720  # default to 720p

    if preferred_res not in res_list:
        # find a resolution that is lower than the preferred resolution
        for res in res_list:
            if preferred_res > res:
                preferred_res = res
                break
        # i really hope you're not desperate enough to download 144p
        # i'm not stopping you though
        preferred_res = max(preferred_res, res_list[-1])

    return preferred_res
