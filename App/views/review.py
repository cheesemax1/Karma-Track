from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
# from App.controllers.user import is_admin
from App.controllers import (
	get_student,
	get_user,
	create_review,
	get_review,
	get_all_reviews,
	get_all_reviews_json,
	get_student_reviews,
	get_lecturer_reviews,
	)

review_views = Blueprint('review_views',
												__name__,
												template_folder='../templates')



@review_views.route('/reviews', methods=['POST'])
def create_review_action():
	data = request.json
	user = get_user(data['lecturer_id'])
	if not user:
			return jsonify({'error' : 'user not found'}),404
	student = get_student(data['student_id'])
	if not student:
			return jsonify({'error' : 'student not found'}),404
	review = create_review(lecturer_id = user.id, student_id = student.id, comment = data['comment'])
	return jsonify({'message': f"review by user {user.id} created for student {student.id}"})

@review_views.route('/reviews/<int:review_id>', methods=['GET'])
def get_review_action(review_id):
	review = get_review(review_id)
	if review:
			return jsonify(review.to_json())
	return jsonify({'error': 'review not found'}),404

@review_views.route('/reviews', methods=['GET'])
@jwt_required()
def get_reviews_action():
	if jwt_current_user.is_admin():
			reviews = get_all_reviews_json()
			return jsonify(reviews)
	return jsonify({'error': 'user not authorised for this operation'}),401


@review_views.route('/reviews/students/<int:student_id>', methods=['GET'])
def get_student_reviews_action(student_id):
	student = get_student(student_id)
	if student:
			reviews = [review.to_json() for review in get_student_reviews(student_id)]
			return jsonify(reviews)
	return jsonify({'error' : 'student not found'}),404

@review_views.route('/reviews/lecturers/<int:lecturer_id>', methods=['GET'])
def get_lecturer_reviews_action(lecturer_id):
	user = get_user(lecturer_id)
	if user:
			reviews = [review.to_json() for review in get_lecturer_reviews(lecturer_id)]
			return jsonify(reviews)
	return jsonify({'error' : 'user not found'}),404