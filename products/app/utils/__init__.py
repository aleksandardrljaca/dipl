from flask import abort


def validate_data(data):
    if not isinstance(data, dict) or len(data) < 4:
        abort(400)

    allowed_keys = {"name", "description", "price", "category_id"}
    if not allowed_keys.issubset(data.keys()):
        abort(400)
