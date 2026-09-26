def is_palindrome_normalized(text):
    normalized = ''.join(
        char.lower() for char in text
        if ('A' <= char <= 'Z') or ('a' <= char <= 'z') or ('0' <= char <= '9')
    )
    return normalized == normalized[::-1]
