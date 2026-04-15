import os
import requests
from flask import Flask, request

app = Flask(__name__)

SERVICE_URL = os.getenv("SERVICE_URL")

@app.route("/backend")
def backend():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return "Unauthorized", 401

    return "Secure backend response"


@app.route("/")
def frontend():
    try:
        # BROKEN: no token
        response = requests.get(f"{SERVICE_URL}/backend")
        return f"Frontend received: {response.text}"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
