from flask import Blueprint, json, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    get_all_users,
    get_all_users_json,
    jwt_required,
    is_admin,
    get_user,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
def get_user_page():
  users = get_all_users()
  return render_template('users.html', users=users)


@user_views.route('/api/users', methods=['GET'])
def get_users_action():
  users = get_all_users_json()
  return jsonify(users)


@user_views.route('/users', methods=['POST'])
def create_user_action():
  data = request.form
  user = create_user(data['username'], data['password'], data['name'],
                     data['user_type'])
  if user:
    return jsonify({'message': f"user {data['username']} created"})
  return jsonify({'error': f"failed to create user {data['username']}"})


@user_views.route('/users/<int:user_id>', methods=['GET'])
def show_user_action(user_id):
  user = get_user(user_id)
  if user:
    return jsonify({'user': user.to_json()})
  return jsonify({'error': f"user {user_id} not found"})