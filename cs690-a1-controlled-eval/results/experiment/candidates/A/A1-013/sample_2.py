def top_k_frequent(items, k):
    counts = {}
    first_seen = {}
    for index, item in enumerate(items):
        counts[item] = counts.get(item, 0) + 1
        if item not in first_seen:
            first_seen[item] = index
    return [
        item
        for item, _ in sorted(
            counts.items(),
            key=lambda pair: (-pair[1], first_seen[pair[0]])
        )[:k]
    ]
