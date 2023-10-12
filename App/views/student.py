from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import (
    create_student, 
    is_admin, 
    update_student_name,
    update_student_year, 
    get_student,
    get_all_students, 
    upvote_student,
    downvote_student, 
    assign_course
    )

student_views = Blueprint('student_views',
                          __name__,
                          template_folder='../templates')


@student_views.route('/students', methods=['POST'])
def create_student_action():
  if is_admin(current_identity.id):
    data = request.form
    student = create_student(data['name'], data['year'])
    if student:
      return jsonify({'message': f"student {data['name']} created"})
    return jsonify({'error': f"failed to create student {data['name']}"})


@student_views.route('/students', methods=['GET'])
def get_students_action():
  if is_admin(current_identity):
    students = get_all_students()
    return jsonify({'students': [student.toJSON() for student in students]})
  return jsonify({'error': 'unauthorized'})


@student_views.route('/students/<int:student_id>', methods=['GET'])
def get_specfic_student_action(student_id):
  student = get_student(student_id)
  if student:
    return jsonify(student)
  return jsonify({'error': 'student not found'})


@student_views.route('/students<int:student_id>', methods=['PUT'])
def update_student_name_action(student_id):
  if is_admin(current_identity.id):
    data = request.form
    student = update_student_name(student_id, data['name'])
    if student:
      return jsonify({'message': f"student {data['name']} updated"})
    return jsonify({'error': f"failed to update student {data['name']}"})


@student_views.route('/students<int:student_id>', methods=['PUT'])
def update_student_year_action(student_id):
  if is_admin(current_identity.id):
    data = request.form
    student = update_student_year(student_id, data['year'])
    if student:
      return jsonify({'message': f"student {data['name']} updated"})
    return jsonify({'error': f"failed to update student {data['name']}"})


@student_views.route('/students<int:student_id>', methods=['PUT'])
def upvote_student_action(student_id):
  student = upvote_student(student_id)
  if student:
    return jsonify({'message': f"student {student_id} upvoted"})
  return jsonify({'error': f"failed to upvote student {student_id}"})


@student_views.route('/students<int:student_id>', methods=['PUT'])
def downvote_student_action(student_id):
  student = downvote_student(student_id)
  if student:
    return jsonify({'message': f"student {student_id} downvoted"})
  return jsonify({'error': f"failed to downvote student {student_id}"})


@student_views.route('/students<int:student_id>', methods=['PUT'])
def assign_course_to_student_action(student_id):
  if is_admin(current_identity.id):
    data = request.form

    student = assign_course(student_id, data['course_id'])
    if student:
      return jsonify({
          'message':
          f"student {student_id} assigned to course {data['course_id']}"
      })
    return jsonify({
        'error':
        f"failed to assign student {student_id} to course {data['course_id']}"
    })
