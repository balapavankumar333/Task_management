from flask import request, jsonify
from app import app, db
from app.models import User
# from flask_bcrypt import check_password_hash_hash

from flask import Blueprint

user_login = Blueprint('user_login', __name__)

@user_login.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "Request must contain JSON data"}), 400

        email = data.get('email')
        password_hash = data.get('password_hash')

        error = None
        if not email or not email.strip() or '@' not in email:
            error = 'Please enter a valid email address'
            return jsonify({"error": error}), 400
        if not password_hash:
            error = 'password_hash is required'
            return jsonify({"error": error}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found. Please check your email and try again."}), 404

        # if not check_password_hash_hash(user.password_hash_hash, password_hash):
        #     return jsonify({"error": "Incorrect password_hash. Please try again."}), 401

        # If the user is authenticated, you can return a success message or a token for authentication.
        return jsonify({"success": "Login successful. Welcome, {}!".format(user.username)}), 200
    except Exception as e:
        error_message = "An error occurred during login: {}".format(str(e))
        return jsonify({"error": error_message}), 500
