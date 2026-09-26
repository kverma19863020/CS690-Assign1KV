def window_sums(values, width):
    if width <= 0:
        raise ValueError("width must be positive")
    if width > len(values):
        return []
    return [
        sum(values[i:i + width])
        for i in range(len(values) - width + 1)
    ]
