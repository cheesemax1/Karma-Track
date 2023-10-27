from App.database import db


class Course(db.Model):
  __tablename__ = 'course'
  course_id = db.Column(db.Integer, primary_key=True)
  lecturer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  course_code = db.Column(db.String(20), unique=True, nullable=False)
  course_name = db.Column(db.String(120), nullable=False)

  def __init__(self, course_code, course_name):
    # self.lecturer_id = lecturer_id
    self.course_code = course_code
    self.course_name = course_name

  def __repr__(self):
    return f'<Code:{self.course_code}, Lecturer :{self.lecturer_id}>'
    
  def assign_lecturer(self, lecturer_id):
    self.lecturer_id = lecturer_id
  
  def to_json(self):
    return {
        "id": self.course_id,
        "lecturer": self.lecturer_id,
        "course_code": self.course_code,
        "course_name": self.course_name
    }
