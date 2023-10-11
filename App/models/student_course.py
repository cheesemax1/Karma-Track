from App.database import db
student_course = db.Table('student_course',
  db.Column ('student_id',db.Integer, db.ForeignKey('student.id')),
  db.Column('course_id',db.ForeignKey('course.course_id'))
)