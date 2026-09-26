def group_anagrams(words):
    groups = {}
    for word in words:
        key = tuple(sorted(word.lower()))
        groups.setdefault(key, []).append(word)
    return list(groups.values())
