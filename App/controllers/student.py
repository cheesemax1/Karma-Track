from App.models import Student, Course
from App.database import db
# from .course import get_course

def create_student(name, year): 
    try:
        student = Student(
            name=name,
            year=year)
        db.session.add(student)
        db.session.commit()
        return student
    except Exception as e:
        print('error creating student', e)
        db.session.rollback()
        return None

def get_student(id):
    return Student.query.get(id)

def update_student_name(id, name):
    student = get_student(id)
    if student:
        student.set_name(name)
        db.session.add(student)
        db.session.commit()
        return student
    return None

def update_student_year(id, year):
    student = get_student(id)
    if student:
        student.set_year(year)
        db.session.add(student)
        db.session.commit()
        return student
    return None

#.first() as student name is not unique
def get_student_by_name(name):
    students = Student.query.filter_by(name=name).first()
    # if not students:
    #     return None
    # students = [student.to_json() for student in students]
    return students

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = get_all_students()
    if not students:
        return []
    students = [student.to_json() for student in students]
    return students

def upvote_student(id):
    student = get_student(id)
    if student:
        student.modify_karma("+")
        db.session.add(student)
        db.session.commit()
        return student
    return None

def downvote_student(id):
    student = get_student(id)
    if student:
        student.modify_karma("-")
        db.session.add(student)
        db.session.commit()
        return student
    return None