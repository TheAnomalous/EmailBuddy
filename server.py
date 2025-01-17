import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# If a user hasn't pinged in this many seconds, they're considered offline
PING_TIMEOUT = 15.0

# We track two users: "A" and "B"
# Example structure:
# {
#   "A": { "color": "black", "count": 0, "last_ping": 0.0 },
#   "B": { "color": "black", "count": 0, "last_ping": 0.0 }
# }
users_data = {
    "A": {"color": "black", "count": 0, "last_ping": 0.0},
    "B": {"color": "black", "count": 0, "last_ping": 0.0},
}

@app.route("/")
def index():
    return "Inbox Count Server is running!"

@app.route("/get_users", methods=["GET"])
def get_users():
    """
    Returns user data for A and B, including a 'count' field
    and an 'online' flag indicating if each user is within
    PING_TIMEOUT of last_ping.

    Sample response:
    {
      "A": {"color": "black", "count": 5, "online": true/false},
      "B": {"color": "red",   "count": 10, "online": true/false}
    }
    """
    now = time.time()
    response = {}

    for user_id in ("A", "B"):
        user = users_data[user_id]

        # Are they online if last ping was within PING_TIMEOUT seconds?
        online = (now - user["last_ping"]) < PING_TIMEOUT

        response[user_id] = {
            "color":  user["color"],
            "count":  user["count"],
            "online": online
        }

    return jsonify(response)

@app.route("/update_user", methods=["POST"])
def update_user():
    """
    POST JSON like:
    {
      "user_id": "A" or "B",
      "color": "black" or "red" (optional),
      "count": <integer> (optional)
    }

    We'll update last_ping so the server knows they're online,
    and update color/count if provided.
    """
    data = request.json or {}
    user_id = data.get("user_id")

    if user_id not in ("A", "B"):
        return jsonify({"error": "Invalid user_id"}), 400

    # Mark user as "just pinged"
    users_data[user_id]["last_ping"] = time.time()

    # Update optional fields
    if "color" in data:
        users_data[user_id]["color"] = data["color"]
    if "count" in data:
        # Store the user's Outlook inbox count
        users_data[user_id]["count"] = data["count"]

    return jsonify({"message": "User updated", "users_data": users_data})

if __name__ == "__main__":
    # For local testing
    app.run(debug=True, port=5000)
