def check_keys(data, keys=[]):
    # return False if any key is missing
    for item in keys:
        if item not in data:
            return False
    # return True if all keys present
    return True