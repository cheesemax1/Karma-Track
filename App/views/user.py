from flask import Blueprint, json, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
  create_admin,
  create_lecturer,
  get_user,
  get_all_users,
  get_all_users_json,
  update_user_name,
  update_user_type,
#   is_admin,
  jwt_authenticate,
  jwt_required,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/lecturer', methods=['POST'])
def create_lecturer_user_action():
    data = request.json
    user = create_lecturer(
        name = data['name'],
        username = data['username'],
        password = data['password'],
    )
    if user:
        return jsonify({'message': f"lecturer account created"}),201
    return jsonify({'error': f"failed to create lecturer account, username already in use"}),401


@user_views.route('/admin', methods=['POST'])
def create_admin_user_action():
    data = request.json
    user = create_admin(
        name = data['name'],
        username = data['username'],
        password = data['password'],
    )
    if user:
        return jsonify({'message': f"admin account created"}),201
    return jsonify({'error': f"failed to create admin account, username already in use"}),401

@user_views.route('/users', methods=['GET'])
@jwt_required()
def get_users_action():
    if jwt_current_user.is_admin():
        users = get_all_users_json()
        return jsonify(users)
    return jsonify({"error":"user not authorized for this operation"}),403
    users = get_all_users_json()
    return jsonify(users)
