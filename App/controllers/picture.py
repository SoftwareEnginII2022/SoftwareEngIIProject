from App.models import Picture
from App.database import db

def upload_Picture(user_id, profile_id, url, likes, dislikes, tierPoints):
    new_Picture = Picture(user_id, profile_id, url, likes, dislikes, tierPoints),
    db.session.add(new_Picture)
    db.session.commit()
    return new_Picture

def get_Picture(id):
    picture = Picture.query.filter_by(id=id).first()
    return picture

def likePicture():



    