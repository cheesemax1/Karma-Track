from App.database import db
from .person import Person
from .student_course import student_course
from datetime import date


class Student(Person):
  __tablename__ = 'student'
  year = db.Column(db.Integer, nullable=False)
  karma = db.Column(db.Integer, default=0)
  reviews = db.relationship('Review', backref=db.backref('student'), lazy = 'joined')
  courses = db.relationship('Course',secondary=student_course,backref='enrolled_students')


def __init__(self, name, year):
  self.name = name
  self.year = year
  self.karma = 0

def __repr__(self):
  return f'<Student :{self.name}, Year :{self.year}, Karma: {self.karma}>'


def toJSON(self):
  return {
      "id": self.id,
      "name": self.name,
      "year": self.year,
      "karma": self.karma,
      "courses" :courses,
      "reviews": reviews
  }
