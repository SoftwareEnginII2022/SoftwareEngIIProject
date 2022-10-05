from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    create_user, 
    create_profile,
    get_all_users,
    get_all_users_json,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    first_name= request.json.get ('first_name')
    last_name = request.json.get ('last_name')

    user = create_user(username, password,first_name,last_name)

    if not user:
        return jsonify({'message': 'An error has occurred or user already exist'},400)
    profile = create_profile(user.id)
    return ({'Message':'user created'}, 201)

@user_views.route('/static/users')
def static_user_page():
  return send_from_directory('static', 'static-user.html')