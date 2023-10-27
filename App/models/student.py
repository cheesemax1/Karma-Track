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
    self.set_year(year)
    self.karma = 0

  def __repr__(self):
    return f'<Student :{self.name}, Year :{self.year}, Karma: {self.karma}>'

  def set_name(self,name):
    self.name = name

  def set_year(self,year):
    if year<0:
      year = 0
    self.year = year

  def modify_karma(self,action):
    if action == "+":
      self.karma+=1
    elif action == "-":
      self.karma-=1  
    else:
      self.karma += 0

  def add_review(self, review):
    self.reviews.append(review)
    
  #TODO: MAKE COURSES A SET OBJECT TO PREVENT DUPLICATES
  def add_course(self,course):
    self.courses.append(course)

  def to_json(self):
    reviews = [review.to_json() for review in self.reviews]
    courses = [course.to_json() for course in self.courses]
    return {
        "id": self.id,
        "name": self.name,
        "year": self.year,
        "karma": self.karma,
        "courses" :courses,
        "reviews": reviews
    }
