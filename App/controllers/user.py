from App.models import User
from App.database import db


def get_all_users():
    return User.query.all()

def create_user(username, password, first_name, last_name):
    newuser = User(username=username, password=password, first_name=first_name, last_name=last_name)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

