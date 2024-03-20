"""
Module for reading the config.yaml file.

Use the get function to get the value of a setting.

config.yaml file is read seperately every time the get function is called to allow
hot swapping values without restarting the server.
"""

import yaml


def get(setting_name: str, default_value=None) -> any:
    """
    Returns the value of the setting with the given name.
    If the setting is not found, returns None, or the default value if it is provided.
    Check the config.yaml file for the type and value of the setting.
    """
    with open("config.yaml", "r", encoding="UTF_8") as file:
        # safe_load is used to prevent code execution from the file
        cfg = yaml.safe_load(file)
        file.close()  # closing the file allows the file to be modified
    try:
        return cfg[setting_name]
    except KeyError:
        return default_value
