from cmath import pi
from App.controllers.picture_details import create_picture_details
from App.controllers.profile import increase_tier_points
from App.models import Picture, Picture_Details, Status
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
        if pic_details.status.name == "Dislike":
            picture.likes =picture.likes + 1 
            picture.dislikes=picture.dislikes - 1                                   
            pic_details.like()
        return picture
    picture.likes = picture.likes +1
    db.session.add(picture)
    db.session.commit()
    pic_details = create_picture_details(picture_id, user_id, "Like")
    increase_tier_points(user_id)
    return picture

def dislike_picture(picture_id, user_id):
    picture = get_picture(picture_id)
    if not picture: 
        return[]
    pic_details = Picture_Details.query.filter_by(picture_id=picture_id, user_id=user_id).first()
    if pic_details:
        if pic_details.status.name == "Like":
            picture.likes = picture.likes - 1
            picture.dislikes =picture.dislikes + 1                                      
            pic_details.dislike()
        return picture
    picture.dislikes = picture.dislikes +1
    db.session.add(picture)
    db.session.commit()
    pic_details = create_picture_details(picture_id, user_id, "Dislike")
    increase_tier_points(user_id)
    return picture

