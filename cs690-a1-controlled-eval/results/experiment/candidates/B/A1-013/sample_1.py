def top_k_frequent(items, k):
    if k == 0:
        return []

    counts = {}
    first_index = {}

    for index, item in enumerate(items):
        if item not in counts:
            counts[item] = 0
            first_index[item] = index
        counts[item] += 1

    ordered = sorted(
        counts,
        key=lambda item: (-counts[item], first_index[item])
    )
    return ordered[:k]
