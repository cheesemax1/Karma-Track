from flask import Blueprint, render_template, jsonify, request, send_from_directory

from App.controllers import (
    get_review, 
    get_all_reviews,
    get_reviews_of_student, 
    get_student,
    get_user, 
    create_review,
    get_reviews_from_lecturer
    )

review_views = Blueprint('review_views',
                         __name__,
                         template_folder='../templates')


@review_views.route('/reviews', methods=['GET'])
def get_reviews_action():
  return jsonify(get_all_reviews())

@review_views.route('/reviews/<int:id>', methods=['GET'])
def get_review_action(id):
  return jsonify(get_review_by_id(id))
  
@review_views.route('/reviews', methods=['POST'])
def create_review_action():
  data = request.form
  student = get_student(data['student_id'])
  reviewer = get_user(data['reviewer_id'])
  review = create_review(reviewer.lecturer_id, student.id,  data['comment'])
  if review:
    return jsonify(
        {'message': f"review by {data['reviewer_id']} created for {student.name}"})
  return jsonify({
      'error':
      f"failed to create review by {data['reviewer_id']} for {student.name}"
  })

@review_views.route('/reviews/<int:student_id>', methods=['GET'])
def get_student_reviews_action(student_id):
  reviews = get_reviews_of_student(student_id)
  return jsonify({'reviews': [review.toJSON() for review in reviews]})


@review_views.route('/reviews/<int:lecturer_id>', methods=['GET'])
def get_lecturer_reviews_action(lecturer_id):
  reviews = get_reviews_from_lecturer(lecturer_id)
  return jsonify({'reviews': [review.toJSON() for review in reviews]})
