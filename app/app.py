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



#### Solution Code ####
# import os
# import requests
# import logging
# from flask import Flask, request

# app = Flask(__name__)

# logging.basicConfig(level=logging.INFO)

# SERVICE_URL = os.getenv("SERVICE_URL", "")

# def get_token():
#     try:
#         token_url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity"

#         headers = {
#             "Metadata-Flavor": "Google"
#         }

#         params = {
#             "audience": SERVICE_URL
#         }

#         response = requests.get(token_url, headers=headers, params=params, timeout=5)
#         response.raise_for_status()

#         return response.text

#     except Exception as e:
#         logging.error(f"Token fetch failed: {str(e)}")
#         return None

# @app.route("/backend")
# def backend():
#     auth_header = request.headers.get("Authorization")

#     if not auth_header:
#         return "Unauthorized", 401

#     if not auth_header.startswith("Bearer "):
#         return "Invalid token", 403

#     return "Secure backend response", 200

# @app.route("/")
# def frontend():
#     try:
#         if not SERVICE_URL:
#             return "ERROR: SERVICE_URL not set in environment", 500

#         token = get_token()

#         if not token:
#             return "ERROR: Failed to retrieve OIDC token", 500

#         headers = {
#             "Authorization": f"Bearer {token}"
#         }

#         response = requests.get(
#             f"{SERVICE_URL}/backend",
#             headers=headers,
#             timeout=5
#         )

#         return f"""
# <div style="font-family: monospace; white-space: pre;">
# ========================================
# Secure Service Call Successful
# ========================================

# Authentication: OIDC Identity Token
# Backend Response: {response.text}

# Result:
# Your Cloud Run service is securely communicating
# using authenticated service-to-service calls.

# ========================================
# </div>
# """

#     except Exception as e:
#         logging.error(f"Frontend error: {str(e)}")
#         return f"Error: {str(e)}", 500

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8080))
#     app.run(host="0.0.0.0", port=port)