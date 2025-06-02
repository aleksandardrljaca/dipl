import requests
from flask import abort
from app.config import services


def extract_service_path(path):
    service_name = path.split("/")[1]
    return services[service_name] + path


def forward_request(url, req):
    response = None
    method = req.method
    headers = dict(req.headers)
    fwd_url = extract_service_path(url)
    match method:
        case "GET":
            response = requests.get(
                fwd_url, headers=headers, params=req.args, verify="cert.crt"
            )
        case "POST":
            response = requests.post(
                fwd_url, headers=headers, json=req.json, verify="cert.crt"
            )
        case "PUT":
            response = requests.put(
                fwd_url, headers=headers, json=req.json, verify="cert.crt"
            )
        case "DELETE":
            response = requests.delete(fwd_url, headers=headers, verify="cert.crt")
        case "PATCH":
            response = requests.patch(
                fwd_url, headers=headers, json=req.json, verify="cert.crt"
            )
        case "OPTIONS":
            response = requests.options(fwd_url, headers=headers, verify="cert.crt")
    return (response.content, response.status_code, response.headers.items())


def validate_payload(data):
    if not isinstance(data, dict):
        abort(400, description="Invalid payload format, expected JSON object.")

    username = data.get("username")
    password = data.get("password")

    if not username:
        abort(400, description="Missing or empty username.")
    if not password:
        abort(400, description="Missing or empty password.")
