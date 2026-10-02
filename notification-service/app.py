from flask import Flask, request, jsonify

app = Flask(__name__)

notifications = []

@app.route('/')
def home():
    return "✅ Notification Service Running Successfully!"

@app.route('/notifications', methods=['GET'])
def get_notifications():
    return jsonify(notifications)

@app.route('/notifications', methods=['POST'])
def send_notification():
    data = request.json
    message = {
        "user_id": data['user_id'],
        "message": data['message']
    }
    notifications.append(message)
    return jsonify({"message": "Notification sent successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6004)
