def rotate_left(items, k):
    if not items:
        return []
    k %= len(items)
    return items[k:] + items[:k]
