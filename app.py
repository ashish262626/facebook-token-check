from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔑 Facebook App Credentials
APP_ID = "YOUR_APP_ID"
APP_SECRET = "YOUR_APP_SECRET"

# Facebook Graph API Endpoints
DEBUG_TOKEN_URL = "https://graph.facebook.com/debug_token"
USER_INFO_URL = "https://graph.facebook.com/me"


# ----------------------------
# ✅ Endpoint: Check a Facebook Token
# ----------------------------
@app.route("/check_token", methods=["POST"])
def check_token():
    """
    Validate a Facebook access token and return user info.
    The client should send: { "access_token": "USER_ACCESS_TOKEN" }
    """
    data = request.get_json()
    if not data or "access_token" not in data:
        return jsonify({"error": "Missing access_token"}), 400

    user_token = data["access_token"]

    # 1️⃣ Check if the token is valid
    params = {
        "input_token": user_token,
        "access_token": f"{APP_ID}|{APP_SECRET}",  # App token for verification
    }

    debug_res = requests.get(DEBUG_TOKEN_URL, params=params)
    debug_data = debug_res.json()

    if "data" not in debug_data:
        return jsonify({"error": "Invalid response from Facebook", "details": debug_data}), 400

    is_valid = debug_data["data"].get("is_valid", False)
    if not is_valid:
        return jsonify({"valid": False, "details": debug_data}), 401

    # 2️⃣ If valid, fetch user info
    user_params = {"access_token": user_token, "fields": "id,name,email"}
    user_res = requests.get(USER_INFO_URL, params=user_params)
    user_data = user_res.json()

    # 3️⃣ Return both validation info and user info
    return jsonify({
        "valid": True,
        "token_debug": debug_data,
        "user_data": user_data
    })


# ----------------------------
# 🏠 Simple route for testing
# ----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Facebook Token Check API",
        "usage": "POST /check_token { access_token: 'FB_USER_TOKEN' }"
    })


# ----------------------------
# 🚀 Run the Flask app
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
