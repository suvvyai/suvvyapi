def _merge_dicts(*dicts: dict) -> dict:
    merged_dict = {}
    for d in dicts:
        merged_dict |= d
    return merged_dict
