from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from.index import index_views

from App.controllers import (
    jwt_authenticate,
    login 
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''


@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
	user = jwt_current_user
	return jsonify({"Current User": f"{user.name}-{user.user_type}"})

@auth_views.route('/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = jwt_authenticate(
    username = data['username'],
    password= data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  return jsonify(access_token=token),200

# @auth_views.route('/login', methods=['POST'])
# def login_action():
#     data = request.json
#     if user:
#         login_user(user)
#         return 'user logged in!'
#     return 'bad username or password given', 401

# @auth_views.route('/logout', methods=['GET'])
# def logout_action():
#     data = request.form
#     user = login(data['username'], data['password'])
#     return 'logged out!'

