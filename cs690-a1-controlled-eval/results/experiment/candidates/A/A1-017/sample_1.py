def is_palindrome_normalized(text):
    normalized = [c.lower() for c in text if ('A' <= c <= 'Z') or ('a' <= c <= 'z') or ('0' <= c <= '9')]
    return normalized == normalized[::-1]
