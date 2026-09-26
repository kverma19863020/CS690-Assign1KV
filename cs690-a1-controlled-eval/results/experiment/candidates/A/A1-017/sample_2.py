def is_palindrome_normalized(text):
    normalized = [c.lower() for c in text if c.isascii() and c.isalnum()]
    return normalized == normalized[::-1]
