import re
import unicodedata


def slugify(value: str) -> str:
    """Slugify

    Args:
        value (str): string to slugify

    Returns:
        str: a slugified string of the value
    """
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")
