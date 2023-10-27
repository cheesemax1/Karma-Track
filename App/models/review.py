from App.database import db
from datetime import datetime


class Review(db.Model):
	__tablename__ = 'review'

	review_id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
	lecturer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	review_date = db.Column(db.DateTime, nullable=False)
	comment = db.Column(db.Text, nullable=False)

	def __init__(self, lecturer_id, student_id, comment):
		self.lecturer_id=lecturer_id
		self.student_id=student_id
		self.review_date = datetime.utcnow()
		self.comment = comment


	def __repr__(self):
		return f'<Reviewer :{self.lecturer_id}, Comment :{self.comment} ,Time of Post: {self.review_date}>'

	def to_json(self):
		review_date = self.review_date
		return {
			"review_id": self.review_id,
			"lecturer": self.lecturer_id,
			"student": self.student_id,
			"review_date": review_date.strftime('%d-%m-%Y'),
			"comment": self.comment
		}
