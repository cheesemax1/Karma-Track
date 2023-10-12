from App.models import Review
from App.database import db
from .user import get_user
from .student import get_student
# from App.models import Student
# from App.models import User


def create_review(user_id, student_id, comment):
  try:
    review = Review(lecturer_id=user_id,
                    student_id=student_id,
                    comment=comment)
    db.session.add(review)
    lecturer = get_user(user_id)
    student = get_student(student_id)
    if lecturer and student:
      lecturer.reviews_made.append(review)
      student.studentreviews.append(review)
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
  reviews = Review.query.all()
  if not reviews:
    return []
  return [review.to_json() for review in reviews]

def get_reviews_of_student(student_id):
  return Review.query.filter(Review.student_id == student_id).all()

def get_reviews_from_lecturer(id):
  return Review.query.filter(Review.lecturer_id == id).all()
