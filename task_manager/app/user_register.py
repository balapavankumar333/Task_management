

from flask import request, jsonify
from app import app, db
from app.models import User
from flask import Blueprint
from app import db, bcrypt

from app.models import User

user_register = Blueprint('user_register', __name__)




@user_register.route('/signup', methods=['POST'])
def Register():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "Request must contain JSON data"}), 400

        email = data.get('email')
        password_hash = data.get('password_hash')
        username = data.get('username')

        error = None
        if not email or not email.strip() or '@' not in email:
            error = 'Please enter a valid email address'
            return jsonify({"error": error}), 400
        if not username or not username.strip():
            error = 'Username is required'
            return jsonify({"error": error}), 400
        if not (len(password_hash) >= 8 and (any(char.isupper() for char in password_hash) or any(char.islower() for char in password_hash))):
            error = 'Password should contain minimum 8 characters and at least one uppercase and one lowercase character'
            return jsonify({"error": error}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": f"User with email '{email}' already exists. Please try with another email."}), 400
        else:
            new_user = User(username=username, email=email, password=password_hash)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"success": "User registered successfully. You can now login with your email and password."}), 201
    except Exception as e:
        error_message = "An error occurred while registering: {}".format(str(e))
        return jsonify({"error": error_message}), 400
