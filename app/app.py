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



#### solution code
# import os  # Used to read environment variables
# import requests  # Used to make HTTP requests (metadata server + backend call)
# import logging  # Used for logging errors and info
# from flask import Flask, request  # Flask framework for web app and request handling

# app = Flask(__name__)  # Create Flask application instance

# logging.basicConfig(level=logging.INFO)  # Set logging level to INFO for debugging

# SERVICE_URL = os.getenv("SERVICE_URL", "")  # Get backend Cloud Run service URL from environment


# def get_token():  # Function to fetch OIDC identity token from metadata server
#     try:  # Start error handling block

#         token_url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity"
#         # Metadata server endpoint for generating identity token

#         headers = {
#             "Metadata-Flavor": "Google"
#         }
#         # Required header to access GCP metadata server

#         params = {
#             "audience": SERVICE_URL
#         }
#         # Audience specifies the target service (Cloud Run URL)

#         response = requests.get(token_url, headers=headers, params=params, timeout=5)
#         # Request OIDC token from metadata server

#         response.raise_for_status()  # Raise error if request fails

#         return response.text  # Return identity token

#     except Exception as e:  # Catch any error during token fetch
#         logging.error(f"Token fetch failed: {str(e)}")  # Log error message
#         return None  # Return None if token retrieval fails


# @app.route("/backend")  # Define backend route (protected service endpoint)
# def backend():

#     auth_header = request.headers.get("Authorization")  # Get Authorization header

#     if not auth_header:  # Check if header is missing
#         return "Unauthorized", 401  # Reject request if no auth header

#     if not auth_header.startswith("Bearer "):  # Validate Bearer token format
#         return "Invalid token", 403  # Reject invalid token format

#     return "Secure backend response", 200  # Return success response if valid


# @app.route("/")  # Define frontend route (caller service)
# def frontend():

#     try:  # Start error handling block

#         if not SERVICE_URL:  # Check if backend URL is configured
#             return "ERROR: SERVICE_URL not set in environment", 500  # Fail if missing

#         token = get_token()  # Fetch OIDC identity token

#         if not token:  # Check if token retrieval failed
#             return "ERROR: Failed to retrieve OIDC token", 500  # Return error

#         headers = {
#             "Authorization": f"Bearer {token}"
#         }
#         # Attach Bearer token for authentication

#         response = requests.get(
#             f"{SERVICE_URL}/backend",  # Backend endpoint URL
#             headers=headers,  # Send authentication header
#             timeout=5  # Request timeout
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
#         # Return formatted HTML response

#     except Exception as e:  # Catch any frontend errors
#         logging.error(f"Frontend error: {str(e)}")  # Log error
#         return f"Error: {str(e)}", 500  # Return error response


# if __name__ == "__main__":  # Entry point of the application

#     port = int(os.environ.get("PORT", 8080))  # Get port from environment (Cloud Run uses 8080)

#     app.run(host="0.0.0.0", port=port)  # Run Flask app on all network interfaces