from flask import Blueprint, request, jsonify,render_template,session
from models.userManagement import UserManager


user_bp = Blueprint("user", __name__)
user_manager = UserManager()


@user_bp.route("/registerpage")
def registerui():
    return render_template('register.html')

@user_bp.route("/loginpage")
def loginui():
    return render_template('login.html')


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400
    success, message = user_manager.register_user(username, password)
    session['username'] = username
    status = 201 if success else 400
    return jsonify({"message": message}), status


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400
    success, message = user_manager.login_user(username, password)
    session['username'] = username
    status = 200 if success else 401
    return jsonify({"message": message}), status
