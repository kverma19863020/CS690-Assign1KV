from collections import OrderedDict

def group_anagrams(words):
    groups = OrderedDict()
    for word in words:
        key = ''.join(sorted(word.lower()))
        groups.setdefault(key, []).append(word)
    return list(groups.values())
