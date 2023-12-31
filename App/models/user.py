from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from .person import Person



class User(Person):         
    __tablename__ = 'user'
    username = db.Column(db.String(120), nullable=False, unique=True)
    user_type = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    courses = db.relationship('Course', backref=db.backref('user'), lazy ='joined')
    reviews = db.relationship('Review', backref=db.backref('user'), lazy ='joined')

    def __init__(self, name, username, password,  user_type):
        self.name = name
        self.username = username
        # self.user_type = user_type
        self.set_user_type(user_type)
        self.set_password(password)

    def __repr__(self):
        return f'<User: {self.id}, {self.name}, {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def set_name(self, name):
        self.name = name

    #to ensure that regardless of input, it is always 'Admin' or 'Lecturer'
    def set_user_type(self, utype):
        self.user_type = utype.title()

    def is_admin(self):
        return self.user_type == 'Admin'
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def add_review(self,review):
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
        "username": self.username,
        "type": self.user_type,
        "courses" : courses,
        "reviews" : reviews
        }


