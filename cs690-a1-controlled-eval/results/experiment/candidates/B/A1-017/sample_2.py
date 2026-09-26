def is_palindrome_normalized(text):
    left = 0
    right = len(text) - 1

    while left < right:
        while left < right and not (
            "A" <= text[left] <= "Z"
            or "a" <= text[left] <= "z"
            or "0" <= text[left] <= "9"
        ):
            left += 1

        while left < right and not (
            "A" <= text[right] <= "Z"
            or "a" <= text[right] <= "z"
            or "0" <= text[right] <= "9"
        ):
            right -= 1

        if text[left].lower() != text[right].lower():
            return False

        left += 1
        right -= 1

    return True
