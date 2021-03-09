def flattened(dictionary, prev_key=''):
    flat = {}
    for key, value in dictionary.items():
        full_key = prev_key + '.' + str(key) if prev_key else key
        if isinstance(value, dict):
            flat.update(flattened(value, full_key))
        elif isinstance(value, list):
            flat.update({full_key + '.' + str(element): True for element in value})
        else:
            flat[full_key] = value
    return flat
