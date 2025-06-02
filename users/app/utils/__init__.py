from flask import abort


def validate_payload(data):
    allowed_keys = {"username", "password", "first_name", "last_name", "age", "role"}

    if not isinstance(data, dict):
        abort(400, description="Data must be a JSON object")

    for key in data:
        if key not in allowed_keys:
            abort(400, description=f"Unexpected field: {key}")

    if "age" in data:
        if not isinstance(data["age"], int) or data["age"] <= 0:
            abort(400, description="Age must be a positive integer")

    for field in ["username", "password", "first_name", "last_name", "role"]:
        if field in data:
            if not isinstance(data[field], str) or not data[field].strip():
                abort(400, description=f"{field} must be a non-empty string")
