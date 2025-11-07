from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 🔑 Facebook App credentials (replace with your own)
APP_ID = "YOUR_APP_ID"
APP_SECRET = "YOUR_APP_SECRET"

# Facebook Graph API v7 endpoints
GRAPH_DEBUG_URL = "https://graph.facebook.com/v7.0/debug_token"
GRAPH_USER_URL = "https://graph.facebook.com/v7.0/me"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check_token", methods=["POST"])
def check_token():
    access_token = request.form.get("access_token")

    if not access_token:
        return render_template("index.html", error="Please enter a Facebook access token.")

    # Validate the token using app access token
    params = {
        "input_token": access_token,
        "access_token": f"{APP_ID}|{APP_SECRET}",
    }
    debug_response = requests.get(GRAPH_DEBUG_URL, params=params)
    debug_data = debug_response.json()

    if "data" not in debug_data:
        return render_template("index.html", error="Invalid response from Facebook.", result=debug_data)

    is_valid = debug_data["data"].get("is_valid", False)
    user_data = {}

    if is_valid:
        # Try to get user info if valid
        user_params = {"access_token": access_token, "fields": "id,name,email"}
        user_response = requests.get(GRAPH_USER_URL, params=user_params)
        user_data = user_response.json()

    return render_template(
        "index.html",
        result=debug_data,
        user=user_data,
        valid=is_valid
    )


if __name__ == "__main__":
    
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')
