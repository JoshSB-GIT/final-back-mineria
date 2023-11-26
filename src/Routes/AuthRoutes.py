from datetime import timedelta
from functools import wraps
from flask import make_response, jsonify, Blueprint, request
from flask_jwt_extended import (
    JWTManager, jwt_required,
    create_access_token, get_jwt_identity, get_jwt
)
from flask_cors import cross_origin
import json
from Models.UserModel import UserModel
from Config.Config import Configuration
from DB.DB import DataBase


auth = Blueprint('auth', __name__)

app = DataBase().app
user_model = UserModel()
SECRET_KEY = Configuration().SECRET_KEY

# Configurar la lista negra
BLOCKLIST_FILE = './src/Tools/blacklist/blacklist.json'
blacklist = set()
try:
    with open(BLOCKLIST_FILE, 'r') as file:
        blacklist = set(json.load(file))
except FileNotFoundError:
    blacklist = set()

# Configurar JWT
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=365 * 10)  # 10 years
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
jwt = JWTManager(app)

# Initialize UserModel
user_model = UserModel()


@auth.route('/login', methods=['POST'])
@cross_origin()
def login():
    code = 200
    access_token = ''
    message = 'Welcome'
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        code = 401
        message = 'Empty user or password'

    # Verify user credentials
    user_data = user_model.verify_user_credentials(email, password)

    if user_data:
        message = 'Successfully verified'
        access_token = create_access_token(identity=user_data)
    else:
        code = 401
        message = 'Invalid credentials'
    return make_response(
        jsonify(
            {"message": message, "data": access_token, "code": code}
        ), code)


@auth.route('/logout', methods=['POST'])
@cross_origin()
@jwt_required()
def logout():
    try:
        current_user = get_jwt_identity()
        jti = get_jwt()['jti']
        blacklist.add(jti)
        save_blacklist()
        code = 200
        message = "Logout successful"

    except Exception as e:
        code = 500
        message = "Error: "+str(e)
    return make_response(
        jsonify(
            {"message": message, "data": current_user, "code": code}
        ), code)


@auth.route('/register', methods=['POST'])
@cross_origin()
@jwt_required()
def register():
    code = 200
    message = 'User added successfully'
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not email or not password or not username:
        code = 400
        message = 'Empty fields'
    user_model = UserModel(email=email, password=password, username=username)
    user_model.add_user()
    return make_response(
        jsonify(
            {"message": message,
             "data": {"email": email,
                      "password": password,
                      "username": username},
             "code": code}
        ), code)


@auth.route('/test', methods=['GET'])
@cross_origin()
@jwt_required()
def test_route():
    try:
        current_user = get_jwt_identity()
        code = 200
        message = "User credentials retrieved successfully"
        data = {
            "email": current_user['email'],
            "username": current_user['username']
        }
    except Exception as e:
        code = 500
        message = "Error: " + str(e)
        data = None

    print(code, message, data)
    return make_response(
        jsonify(
            {"message": message, "data": data, "code": code}
        ), code)


def save_blacklist():
    with open(BLOCKLIST_FILE, 'w') as file:
        json.dump(list(blacklist), file)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(type, decoded_token):
    print(decoded_token, type)
    jti = decoded_token['jti']
    return jti in blacklist
