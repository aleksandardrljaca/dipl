from flask import abort
from flask import abort


def validate_payload(data):
    if not isinstance(data, dict):
        abort(400, description="Payload must be a JSON object")

    required_keys = {"name", "description"}
    if not required_keys.issubset(data.keys()):
        abort(
            400, description=f"Missing required fields: {required_keys - data.keys()}"
        )

    for k in data.keys():
        if k not in required_keys:
            abort(400, description=f"Invalid field: {k}")

    for k in required_keys:
        if not isinstance(data[k], str) or not data[k].strip():
            abort(400, description=f"Field '{k}' must be a non-empty string")
