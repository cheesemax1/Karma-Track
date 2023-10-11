from App.database import db
from datetime import datetime


class Review(db.Model):
  __tablename__ = 'review'

  review_id = db.Column(db.Integer, primary_key=True)
  student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
  lecturer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  review_date = db.Column(db.Date, default=datetime.utcnow)
  comment = db.Column(db.Text, nullable=False)

  def __init__(self, lecturer_id, student_id, comment):
    self.lecturer_id = lecturer_id
    self.student_id = student_id
    self.comment = comment

  def __repr__(self):
    return f'<Reviewer :{self.lecturer_id}, Comment :{self.comment}>'

  def toJSON(self):
    return {
        'Lecturer': self.lecturer_id,
        'Student': self.student_id,
        'reviewDate': self.review_date.strftime('%Y-%m-%d'),
        'comment': self.comment
    }
