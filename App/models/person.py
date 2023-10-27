from App.database import db


class Person(db.Model):
  __abstract__ = True
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)

  def __init__(self, name):
    self.name = name

  def to_json(self):
    return {"id": self.id, "name": self.name}
