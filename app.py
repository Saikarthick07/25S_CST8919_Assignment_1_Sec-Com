from flask import Flask, request, jsonify, session
from functools import wraps
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Securely load secret key from environment variable
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-insecure-key')  # fallback for dev only

logging.basicConfig(level=logging.INFO)

def log_event(level, event_type, username=None, path=None, message=None):
    timestamp = datetime.utcnow().isoformat()
    log_msg = f"{event_type}: username={username}, timestamp={timestamp}, path={path}, message={message}"
    if level == "info":
        app.logger.info(log_msg)
    else:
        app.logger.warning(log_msg)

# Auth simulation
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "password123":
        session['user'] = username
        log_event("info", "LOGIN_SUCCESS", username=username, path="/login", message="Login successful")
        return jsonify({"message": "Login successful"}), 200
    else:
        log_event("warning", "LOGIN_FAILURE", username=username, path="/login", message="Login failed")
        return jsonify({"message": "Login failed"}), 401

# Auth decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            log_event("warning", "UNAUTHORIZED_ACCESS", username=None, path=request.path, message="Missing session user")
            return jsonify({"message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/protected')
@requires_auth
def protected():
    username = session.get('user')
    log_event("info", "PROTECTED_ACCESS", username=username, path="/protected", message="Accessed protected route")
    return jsonify({"message": f"Hello {username}, you accessed protected content!"}), 200

@app.errorhandler(401)
def unauthorized(e):
    log_event("warning", "ERROR_401", path=request.path, message="Unauthorized error handler triggered")
    return jsonify({"message": "Unauthorized"}), 401

if __name__ == "__main__":
    app.run()
