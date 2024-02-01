"""
Utility function to format the title of a video to be suitable for filenames.
"""


def format_title(title: str, remove_spaces: bool = False) -> str:
    """
    Formats the title to be suitable for filenames

    Args:
        title: the string to format
        remove_spaces: replace spaces with underscores if set to True
    """
    # not adding these three lines are a great way learn from mistakes, trust me
    title = title.replace(':', '').replace(
        "\\", '').replace("/", '').replace(".", '')

    # luckily spaces are allowed in filenames, but i'll leave the choice to you
    # just set remove_spaces to True if you want to remove spaces.
    # this won't be added to the config file, because it's not that important
    # but if you're reading this, you can add it yourself if you want to
    if remove_spaces:
        title = title.replace(" ", "_")

    # cyrillic characters work fine, but for the sake of consistency,
    # we'll replace them with latin characters
    def cyrillic_to_latin(text: str):
        """
        Replaces cyrillic letters in the passed string with latin letters
        """
        cyrillic_to_latin_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
            'ы': 'y', 'э': 'e', 'ю': 'iu', 'я': 'ia'
        }
        return ''.join(cyrillic_to_latin_map.get(char.lower(), char) for char in text)

    title = cyrillic_to_latin(title)

    return title
