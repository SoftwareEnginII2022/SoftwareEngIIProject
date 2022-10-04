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

def likePicture(picture_id, user_id):
    picture = get_Picture(picture_id)
    if not picture: 
        return[]
    pic_Details = Picture_Details.query.filter_by(picture_id=picture_id, user_id=user_id).first()
    if pic_Details:                                   
        pic_Details.like()
        return picture
    pic_Details = create_Picture_Details(picture_id, user_id, "Like")
    return picture

def dislikePicture(picture_id, user_id):
    picture = get_Picture(picture_id)
    if not picture: 
        return[]
    pic_Details = Picture_Details.query.filter_by(picture_id=picture_id, user_id=user_id).first()
    if pic_Details:                                   
        pic_Details.dislike()
        return picture
    pic_Details = create_Picture_Details(picture_id, user_id, "Dislike")
    return picture

