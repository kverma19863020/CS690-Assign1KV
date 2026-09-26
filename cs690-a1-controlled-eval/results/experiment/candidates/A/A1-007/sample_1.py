def longest_run(items):
    if not items:
        return 0

    longest = current = 1
    previous = items[0]

    for item in items[1:]:
        if item == previous:
            current += 1
        else:
            current = 1
            previous = item
        if current > longest:
            longest = current

    return longest
