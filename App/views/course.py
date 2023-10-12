from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers.user import is_admin
from App.controllers.course import (
    create_course, 
    get_course, 
    get_lecturer_courses, 
    get_student_courses, 
    get_all_courses
    )

course_views = Blueprint('course_views', __name__, template_folder='../templates')

@course_views.route('/courses', methods=['POST'])
def create_course_action():
  if is_admin(current_identity.id):
    data = request.form
    course = create_course(data['lecturer_id'], data['course_code'], data['course_name'])
    if course:
      return jsonify({'message': f"course {data['course_code']} created"})
    return jsonify({'error': f"failed to create course {data['course_code']}"})

@course_views.route('/courses', methods=['GET'])
def show_all_courses_action():
  if is_admin(current_identity.id):
    courses = get_all_courses()
    return jsonify({'courses': [course.toJSON() for course in courses]})
  return jsonify({'error': 'unauthorized'})

@course_views.route('/courses/<int:student_id>', methods=['GET'])
def show_all_courses_student_action(student_id):
  if is_admin(current_identity.id):
    courses = get_student_courses(student_id)
    return jsonify({'courses': [course.toJSON() for course in courses]})
  return jsonify({'error': 'unauthorized'})

@course_views.route('/courses/<int:lecturer_id>', methods=['GET'])
def show_all_courses_lecturer_action(lecturer_id):
  if is_admin(current_identity.id):
    courses = get_lecturer_courses(lecturer_id)
    return jsonify({'courses': [course.toJSON() for course in courses]})
  return jsonify({'error': 'unauthorized'})
