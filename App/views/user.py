from flask import Blueprint, json, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
  create_user,
  get_user,
#   get_user_by_username,
  get_all_users,
  get_all_users_json,
  update_user,
  is_admin,
  jwt_authenticate,
  jwt_required,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/lecturer', methods=['POST'])
def create_lecturer_user_action():
    data = request.json
    user = create_user(
        name = data['name'],
        username = data['username'],
        password = data['password'],
        user_type = 'Lecturer'
    )
    if user:
        return jsonify({'message': f"lecturer account created"}),201
    return jsonify({'error': f"failed to create lecturer account, username already in use"}),401


@user_views.route('/admin', methods=['POST'])
def create_admin_user_action():
    data = request.json
    user = create_user(
        name = data['name'],
        username = data['username'],
        password = data['password'],
        user_type = 'Admin'
    )
    if user:
        return jsonify({'message': f"admin account created"}),201
    return jsonify({'error': f"failed to create admin account, username already in use"}),401

# @user_views.route('/identify', methods=['GET'])
# @jwt_required()
# def identify_user_action():
#     user = jwt_current_user
#     return jsonify({"Current User": user.toJSON()})

@user_views.route('/users', methods=['GET'])
@jwt_required()
def get_users_action():
    if is_admin(jwt_current_user.id):
        users = get_all_users_json()
        return jsonify(users)
    return jsonify({"error":"user not authorized for this operation"}),403