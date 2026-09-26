def longest_run(items):
    if not items:
        return 0

    longest = current = 1
    for previous, value in zip(items, items[1:]):
        if value == previous:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest
