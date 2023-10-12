from App.models import Student
from App.database import db

def create_student(name, year):
  try:
    student = Student(name=name, year=year)
    db.session.add(student)
    db.session.commit()
    return student
  except Exception as e:
    print('error creating student', e)
    db.session.rollback()
    return None

def update_student_name(id, name):
  student = get_student(id)
  if student:
    student.name = name
    db.session.add(student)
    return db.session.commit()
  return None


def update_student_year(id, year):
  student = get_student(id)
  if student:
    student.year = year
    db.session.add(student)
    return db.session.commit()
  return None

def get_student(id):
  return Student.query.get(id)

#.all() as student name is not unique
def get_student_by_name(name):
    return Student.query.filter(Student.name == name).all()

def get_all_students():
  return Student.query.all()

def upvote_student(id):
  student = get_student(id)
  if student:
    student.karma += 1
    db.session.add(student)
    return db.session.commit()
  return None

def downvote_student(id):
  student = get_student(id)
  if student:
    student.karma -= 1
    db.session.add(student)
    return db.session.commit()
  return None