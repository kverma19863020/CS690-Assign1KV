def chunked(items, size):
    if size <= 0:
        raise ValueError("size must be greater than 0")
    return [list(items[i:i + size]) for i in range(0, len(items), size)]
