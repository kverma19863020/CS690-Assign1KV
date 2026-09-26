def parse_bool(text):
    value = text.strip().casefold()
    if value in ("true", "1", "yes", "on"):
        return True
    if value in ("false", "0", "no", "off"):
        return False
    raise ValueError(f"invalid boolean value: {text!r}")
