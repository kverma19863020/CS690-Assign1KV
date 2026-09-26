def clamp_int(x, lower, upper):
    return lower if x < lower else upper if x > upper else x
