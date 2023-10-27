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
    
    lecturer = get_user(lecturer_id)
    student = get_student(student_id)
    if lecturer and student:
      # db.session.add(review)
      lecturer.add_review(review)
      student.add_review(review)
      db.session.add_all({review,lecturer,student})
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
  return [review.to_json() for review in reviews]

def get_student_reviews(student_id):
  return Review.query.filter(Review.student_id == student_id).all()

def get_lecturer_reviews(lecturer_id):
  return Review.query.filter(Review.lecturer_id == lecturer_id).all()