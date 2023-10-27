from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import (
        create_student,
        update_student_name,
        update_student_year,
        get_student,
        get_student_by_name,
        get_all_students_json,
        upvote_student,
        downvote_student,
        assign_course_student,
        # is_admin
        )

student_views = Blueprint('student_views',__name__,template_folder='../templates')


@student_views.route('/students', methods=['POST'])
@jwt_required()
def create_student_action():
    if jwt_current_user.is_admin():
        data = request.json
        student = create_student(data['name'], data['year'])
        return jsonify({'message': f"student created"}),201 
    return jsonify({'error': 'user not authorised for this operation'}),401

@student_views.route('/students/<student_id>', methods=['GET'])
def get_student_by_id_action(student_id):
    student = get_student(student_id)
    if student:
        return jsonify(student.to_json()),200
    return jsonify({'error': 'student not found'}),404

@student_views.route('/students/<student_name>', methods=['GET'])
def get_student_by_name_action(student_name):
    student = get_student_by_name(student_name)
    if student:
        return jsonify(student.to_json()),200
    return jsonify({'error': 'student not found'}),404

@student_views.route('/students', methods=['GET'])
@jwt_required()
def get_students_action():
    if jwt_current_user.is_admin():
        students = get_all_students_json()
        return jsonify(students)
    return jsonify({'error': 'user not authorised for this operation'}),401

@student_views.route('/students/name/<student_id>', methods=['PUT'])
@jwt_required()
def update_student_name_action(student_id):
    if jwt_current_user.is_admin():
        data = request.json
        student = update_student_name(student_id, data['name'])
        if student:
            return jsonify({'message': f"student updated"}),201
        return jsonify({'error': f"student not found"}),404
    return jsonify({'error': 'user not authorised for this operation'}),401


@student_views.route('/students/year/<student_id>', methods=['PUT'])
@jwt_required()
def update_student_year_action(student_id):
    if jwt_current_user.is_admin():
        data = request.json
        if data['year'] >= 1:
            student = update_student_year(student_id, data['year'])
            if student:
                return jsonify({'message': f"student updated"}),201
            return jsonify({'error': f"student not found"}),404
        return jsonify({'error':'new year entered < 1'}),400
    return jsonify({'error': 'user not authorised for this operation'}),401

@student_views.route('/students/up/<student_id>', methods=['PUT'])
def upvote_student_action(student_id):
    student = upvote_student(student_id)
    if student:
        return jsonify({'message': f"student upvoted"}),201
    return jsonify({'error': f"student not found"}),404


@student_views.route('/students/down/<student_id>', methods=['PUT'])
def downvote_student_action(student_id):
    student = downvote_student(student_id)
    if student:
        return jsonify({'message': f"student downvoted"}),201
    return jsonify({'error': f"student not found"}),404