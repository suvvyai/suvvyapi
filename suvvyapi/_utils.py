from typing import Any


def _merge_dicts(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    merged_dict: dict[Any, Any] = {}
    for d in dicts:
        merged_dict |= d
    return merged_dict
