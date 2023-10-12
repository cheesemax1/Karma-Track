from App.models import Course
from App.database import db
from .user import get_user

def create_course(lecturer_id, course_code, course_name):

 try:
  course = Course(lecturer_id=lecturer_id, course_code=course_code, course_name=course_name)
  db.session.add(course)
  lecturer = get_user(lecturer_id)
  if not lecturer:
    return None
  lecturer.courses_teaching.append(course)
  db.session.commit()
  return course
 except Exception as e:
   print('error in creating course:',e)
   db.session.rollback()
   return None

def get_course(id):
  course = Course.query.get(id)
  if course:
    return course
  return None



def get_lecturer_courses(lecturer_id):
    return Course.query.filter_by(lecturer_id=lecturer_id).all()
  
def get_student_courses(student_id):
  return Course.query.filter_by(students=student_id).all()

def get_all_courses():
  return Course.query.all()

def get_all_courses_json():
    courses = Course.query.all()
    if not courses:
        return []
    courses = [courses.toJSON() for course in courses]
    return courses

