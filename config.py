"""
Module for reading the config.yaml file.

Use the get function to get the value of a setting.

config.yaml file is read seperately every time the get function is called to allow
hot swapping values without restarting the server.
"""

import yaml


def get(setting_name: str) -> any:
    """
    Returns the value of the setting with the given name.
    Returns 4 different types of values depending on setting, so type hinting will be hardly useful.
    Hence, the return type is set to any.
    Check the config.yaml file for the type and value of the setting.
    """
    with open("config.yaml", "r", encoding="UTF_8") as file:
        # safe_load is used to prevent code execution from the file
        cfg = yaml.safe_load(file)
        file.close()  # closing the file allows the file to be modified
    return cfg[setting_name]
