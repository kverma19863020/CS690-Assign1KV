def longest_run(items):
    if not items:
        return 0

    longest = 1
    current = 1

    for i in range(1, len(items)):
        if items[i] == items[i - 1]:
            current += 1
        else:
            current = 1
        if current > longest:
            longest = current

    return longest
