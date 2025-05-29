from typing import Any


def remove_none_and_empty_items(values: dict[Any, Any]) -> dict[Any, Any]:
    new_values = {k: v for k, v in values.items() if v is not None and v != ""}
    return new_values
