from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# 🔑 Facebook App Credentials (replace with your real ones)
APP_ID = "YOUR_APP_ID"
APP_SECRET = "YOUR_APP_SECRET"

# Facebook Graph API endpoints
DEBUG_TOKEN_URL = "https://graph.facebook.com/debug_token"
USER_INFO_URL = "https://graph.facebook.com/me"


@app.route("/")
def home():
    """
    Render the HTML home page with a form to input access token.
    """
    return render_template("index.html")


@app.route("/check_token", methods=["POST"])
def check_token():
    """
    Validate the Facebook access token and display result.
    """
    access_token = request.form.get("access_token")

    if not access_token:
        return render_template("index.html", error="Please enter a Facebook access token.")

    # Step 1: Validate the token
    params = {
        "input_token": access_token,
        "access_token": f"{APP_ID}|{APP_SECRET}",  # App access token for validation
    }
    debug_response = requests.get(DEBUG_TOKEN_URL, params=params)
    debug_data = debug_response.json()

    # If the response is invalid
    if "data" not in debug_data:
        return render_template("index.html", error="Invalid response from Facebook.", result=debug_data)

    is_valid = debug_data["data"].get("is_valid", False)

    # Step 2: If valid, fetch user info
    user_data = {}
    if is_valid:
        user_params = {"access_token": access_token, "fields": "id,name,email"}
        user_response = requests.get(USER_INFO_URL, params=user_params)
        user_data = user_response.json()

    # Step 3: Return rendered page with result
    return render_template(
        "index.html",
        result=debug_data,
        valid=is_valid,
        user=user_data
    )


if __name__ == "__main__":
    app.run(debug=True, if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')
