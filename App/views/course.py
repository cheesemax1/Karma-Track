from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers.user import is_admin
from App.controllers.course import (
		create_course,
		get_course,
		assign_course_lecturer,
		assign_course_student,
		get_lecturer_courses,
		get_student_courses,
		get_all_courses,
		get_all_courses_json,
		get_student,
		get_user
		)

course_views = Blueprint('course_views', __name__, template_folder='../templates')

@course_views.route('/courses', methods=['POST'])
@jwt_required()
def create_course_action():
	if is_admin(jwt_current_user.id):
		data = request.json
		course = create_course( 
			data['course_code'], 
			data['course_name']
			)
		if course:
			return jsonify({'message': f"course {data['course_code']} created"}),201
		return jsonify({'error': f"failed to create course {data['course_code']}"}),400

@course_views.route('/courses/<int:course_id>', methods=['GET'])
def show_course_given_id_action(course_id):
	course = get_course(course_id)
	if course:
		return jsonify(course.toJSON()),200
	return jsonify({'error':f"course not found"}),404

@course_views.route('/courses', methods=['GET'])
@jwt_required()
def show_all_courses_action():
	if is_admin(jwt_current_user.id):
		courses = get_all_courses_json()
		return jsonify(courses)
		# return jsonify({'courses': [course.toJSON() for course in courses]}),200
	return jsonify({'error': 'user not authorized for this operation'}),401

@course_views.route('/courses/<student_id>', methods=['GET'])
# @jwt_required()
def show_all_courses_student_action(student_id):
	student = get_student(student_id)
	if not student:
		return jsonify(
			{'error': f"student not found"}),404	
	courses = get_student_courses(student_id)
	return jsonify(
		{'courses': [course.toJSON() for course in courses]}),200

@course_views.route('/courses/<lecturer_id>', methods=['GET'])
def show_all_courses_lecturer_action(lecturer_id):
	user = get_user(lecturer_id)
	if not user:
		return jsonify(
			{'error': f"User not found"}),404	
	courses = get_lecturer_courses(lecturer_id)
	return jsonify(
		{'courses': [course.toJSON() for course in courses]}),200

@course_views.route('/courses/lecturer',methods=['PUT'])
@jwt_required()
def assign_course_lecturer_action():
	if is_admin(jwt_current_user.id):
		data = request.json
		course_id = data['course_id']
		lecturer_id = data['lecturer_id']
		if not get_course(course_id):
			return jsonify({"error":f"course not found"}),404
		if not get_user(lecturer_id):
			return jsonify({"error":f"user not found"}),404
		course = assign_course_lecturer(
			id = course_id,
			lecturer_id = lecturer_id
		)
		return jsonify(
			{"message":f"course {course_id} assigned to user {lecturer_id}"}
			),201
	return jsonify({"error":"user not authorized for this operation"}),403

@course_views.route('/courses/student',methods=['PUT'])
@jwt_required()
def assign_course_student_action():
	if is_admin(jwt_current_user.id):
		data = request.json
		course_id = data['course_id']
		student_id = data['student_id']
		if not get_course(course_id):
			return jsonify({"error":f"course {course_id} not found"}),404
		if not get_user(student_id):
			return jsonify({"error":f"student {student_id} not found"}),404
		course = assign_course_student(
			id = course_id,
			student_id = student_id
		)
		return jsonify(
			{"message":f"course {course_id} assigned to student {student_id}"}
			),201
	return jsonify({"error":"user not authorized for this operation"}),403
	
