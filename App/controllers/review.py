from App.models import Review
from App.database import db
from .user import get_user
from .student import get_student
# from App.models import Student
# from App.models import User


def create_review(lecturer_id, student_id, comment):
  try:
    review = Review(lecturer_id=lecturer_id,
                    student_id=student_id,
                    comment=comment)
    db.session.add(review)
    lecturer = get_user(lecturer_id)
    student = get_student(student_id)
    if lecturer and student:
      lecturer.reviews.append(review)
      student.reviews.append(review)
      db.session.commit()
      return review
  except Exception as e:
    print("Error creating review", e)
    db.session.rollback()
    return None

def get_review(id):
  review = Review.query.get(id)
  if review :
      return review
  return None

def get_all_reviews():
  return Review.query.all()

def get_all_reviews_json():
  reviews = get_all_reviews()
  if not reviews:
    return []
  return [review.toJSON() for review in reviews]

def get_student_reviews(student_id):
  return Review.query.filter(Review.student_id == student_id).all()

def get_lecturer_reviews(lecturer_id):
  return Review.query.filter(Review.lecturer_id == lecturer_id).all()