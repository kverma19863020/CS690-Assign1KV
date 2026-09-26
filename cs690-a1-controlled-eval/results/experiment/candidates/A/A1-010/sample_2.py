def word_counts(text):
    import string

    punctuation = '.,;:!?"\'()[]{}'
    return {
        token: normalized_tokens.count(token)
        for token in (normalized_tokens := [
            raw_token.lower().strip(punctuation)
            for raw_token in text.split()
        ])
        if token
    }
