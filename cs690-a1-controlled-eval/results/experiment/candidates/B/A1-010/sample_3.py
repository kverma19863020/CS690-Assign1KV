def word_counts(text):
    punctuation = ".,;:!?\"'()[]{}"
    counts = {}
    for token in text.split():
        normalized = token.lower().strip(punctuation)
        if normalized:
            counts[normalized] = counts.get(normalized, 0) + 1
    return counts
