import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# If a user hasn't pinged in this many seconds, they're considered offline
PING_TIMEOUT = 15.0

# We track two users: "A" and "B"
# Example structure:
# {
#   "A": { "initial": "A", "color": "black", "last_ping": 0.0 },
#   "B": { "initial": "B", "color": "black", "last_ping": 0.0 }
# }
users_data = {
    "A": {"initial": "A", "color": "black", "last_ping": 0.0},
    "B": {"initial": "B", "color": "black", "last_ping": 0.0},
}

@app.route("/")
def index():
    return "Inbox Count Server is running!"

@app.route("/get_users", methods=["GET"])
def get_users():
    """
    Returns user data for A and B, plus an 'online' flag indicating if
    each user is within PING_TIMEOUT of last_ping.
    {
      "A": {"initial": "A", "color": "black", "online": true/false},
      "B": {"initial": "B", "color": "black", "online": true/false}
    }
    """
    now = time.time()
    response = {}

    for user_id in ("A", "B"):
        u = users_data[user_id]
        # Are they online?
        is_online = (now - u["last_ping"]) < PING_TIMEOUT
        response[user_id] = {
            "initial": u["initial"],
            "color":   u["color"],
            "online":  is_online
        }

    return jsonify(response)

@app.route("/update_user", methods=["POST"])
def update_user():
    """
    POST JSON like:
    {
      "user_id": "A" or "B",
      "initial": <optional>,
      "color": <optional>
    }
    We'll also update last_ping so the server knows they're online.
    """
    data = request.json or {}
    user_id = data.get("user_id")
    if user_id not in ("A", "B"):
        return jsonify({"error": "Invalid user_id"}), 400

    # Mark them as just pinged
    users_data[user_id]["last_ping"] = time.time()

    # Update optional fields
    if "initial" in data and data["initial"]:
        users_data[user_id]["initial"] = data["initial"]
    if "color" in data and data["color"]:
        users_data[user_id]["color"] = data["color"]

    return jsonify({"message": "User updated", "users_data": users_data})

if __name__ == "__main__":
    # For local testing
    app.run(debug=True, port=5000)
