import bleach


def sanitize_input(value: str) -> str:
    """Removes dangerous HTML and leading/trailing spaces"""
    return bleach.clean(value.strip(), tags=[], strip=True)
