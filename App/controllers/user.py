from App.models import User
from App.database import db


def create_admin(name, username, password):
  try:
    newuser = User(name=name,
                   username=username,
                   password=password,
                   user_type="Admin")
    db.session.add(newuser)
    db.session.commit()
    return newuser
  except Exception as e:
    print('error in creating Admin user: ', e)
    db.session.rollback()
    return None
    
def create_lecturer(name, username, password):
  try:
    newuser = User(name=name,
                   username=username,
                   password=password,
                   user_type="Lecturer")
    db.session.add(newuser)
    db.session.commit()
    return newuser
  except Exception as e:
    print('error in creating Lecturer user: ', e)
    db.session.rollback()
    return None

def get_user(id):
    user = User.query.get(id)
    if user :
        return user
    return None

def get_user_by_username(username):
    user = User.query.filter_by(username = username).first()
    return user

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.to_json() for user in users]
    return users

def update_user_name(id, newname):
    user = get_user(id)
    if user:
        user.set_name(newname)
        db.session.add(user)
        db.session.commit()
        return user
    return None

def update_user_type(id, newtype):
    user = get_user(id)
    if user:
        user.set_user_type(newtype)
        db.session.add(user)
        db.session.commit()
        return user
    return None

# def is_admin(id):
#   user = get_user(id)
#   return user.is_admin()


  