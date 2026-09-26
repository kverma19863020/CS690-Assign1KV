def stable_partition(items, pivot):
    return [item for item in items if item < pivot] + [
        item for item in items if item >= pivot
    ]
