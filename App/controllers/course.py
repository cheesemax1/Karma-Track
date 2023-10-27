from App.models import Course, Student
from App.database import db
from .user import get_user
from .student import get_student


def create_course(course_code, course_name):
  try:
    course = Course(course_code=course_code,
                    course_name=course_name)
    db.session.add(course)
    db.session.commit()
    return course
  except Exception as e:
    print('error in creating course:', e)
    db.session.rollback()
    return None

def get_course(id):
  course = Course.query.get(id)
  if course :
    return course
  return None

def assign_course_lecturer(id,lecturer_id):
  course = get_course(id)
  lecturer = get_user(lecturer_id)
  if (course and lecturer):
    course.assign_lecturer(lecturer_id)
    lecturer.add_course(course)
    db.session.add_all({course,lecturer})
    db.session.commit()
    return course
  return None

def assign_course_student(id,student_id):
	course = get_course(id)
	# course = Course.query.get(course_id)
	student = get_student(student_id)
	if course and student:
		student.add_course(course)
		db.session.add(student)
		db.session.commit()
		return course
	return None  

  
def get_lecturer_courses(lecturer_id): #gets all the courses taught by given lecturer
  return Course.query.filter_by(lecturer_id=lecturer_id).all()
  
def get_student_courses(student_id): #gets all the courses a given student is currently enrolled in
  student = get_student(student_id)
  return student.courses

def get_enrolled_students(id): # gets all students enrolled in a course
  course = get_course(id)
  if course:
    return course.enrolled_students
  return None


def get_all_courses():
  return Course.query.all()

def get_all_courses_json():
  courses = get_all_courses()
  if not courses:
    return []
  courses = [course.to_json() for course in courses]
  return courses