from App.models import Course
from App.database import db
from .user import get_user

def create_course(lecturer_id, course_code, course_name):
  course = Course(lecturer_id=lecturer_id, course_code=course_code, course_name=course_name)
  db.session.add(course)
  lecturer = get_user(lecturer_id)
  