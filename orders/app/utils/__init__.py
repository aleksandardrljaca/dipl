from flask import abort


def validate_data(data):
    if not isinstance(data, list) or not data:
        abort(400)

    for item in data:
        if not isinstance(item, dict):
            abort(400)
        if "id" not in item or "quantity" not in item:
            abort(400)
