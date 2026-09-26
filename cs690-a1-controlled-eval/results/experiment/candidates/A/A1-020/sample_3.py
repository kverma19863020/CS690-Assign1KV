def summarize_ranges(nums):
    result = []
    if not nums:
        return result

    start = prev = nums[0]
    for number in nums[1:]:
        if number != prev + 1:
            result.append(str(start) if start == prev else f"{start}-{prev}")
            start = number
        prev = number

    result.append(str(start) if start == prev else f"{start}-{prev}")
    return result
