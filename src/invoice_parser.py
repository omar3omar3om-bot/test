import json
from typing import Any, Dict, List


def _default_schema() -> Dict[str, Any]:
    return {
        "vendor": None,
        "date": None,
        "total": None,
        "line_items": [],
    }


def normalize_invoice_output(raw_text: str) -> Dict[str, Any]:
    schema = _default_schema()
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        schema["raw_output"] = raw_text
        return schema

    if not isinstance(data, dict):
        schema["raw_output"] = raw_text
        return schema

    schema["vendor"] = data.get("vendor")
    schema["date"] = data.get("date")
    schema["total"] = data.get("total")

    line_items = data.get("line_items", [])
    if isinstance(line_items, list):
        schema["line_items"] = _normalize_line_items(line_items)
    else:
        schema["line_items"] = []

    return schema


def _normalize_line_items(items: List[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "description": item.get("description"),
                "quantity": item.get("quantity"),
                "unit_price": item.get("unit_price"),
                "line_total": item.get("line_total"),
            }
        )
    return normalized
