from App.models import Picture, Picture_Details
from App.database import db

def upload_picture(user_id, profile_id, url):
    picture = Picture(user_id = user_id,profile_id=profile_id, url = url)
    db.session.add(picture)
    db.session.commit()
    return picture

def get_picture(id):
    picture = Picture.query.filter_by(id=id).first()
    if not picture:
        return []
    return picture

def like_picture(picture_id, user_id):
    picture = get_picture(picture_id)
    if not picture: 
        return[]
    pic_details = Picture_Details.query.filter_by(picture_id=picture_id, user_id=user_id).first()
    if pic_details:                                   
        pic_details.like()
        return picture
    pic_details = create_picture_details(picture_id, user_id, "Like")
    return picture

def dislike_picture(picture_id, user_id):
    picture = get_picture(picture_id)
    if not picture: 
        return[]
    pic_details = Picture_Details.query.filter_by(picture_id=picture_id, user_id=user_id).first()
    if pic_details:                                   
        pic_details.dislike()
        return picture
    pic_details = create_picture_details(picture_id, user_id, "Dislike")
    return picture

