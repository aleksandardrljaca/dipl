from flask import abort


def validate_data(data):
    if type(data) is not dict:
        abort(400)
    elif len(data) < 2:
        abort(400)
    else:
        for k, v in data.items():
            if k not in ["product_id", "review"]:
                abort(400)
