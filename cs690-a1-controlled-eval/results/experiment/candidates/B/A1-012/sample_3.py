def transpose_rectangular(matrix):
    if not matrix:
        return []
    row_length = len(matrix[0])
    if any(len(row) != row_length for row in matrix):
        raise ValueError("row lengths differ")
    if row_length == 0:
        return []
    return [[row[column] for row in matrix] for column in range(row_length)]
