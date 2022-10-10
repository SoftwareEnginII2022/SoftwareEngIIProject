from App.models import Picture_Details
from App.database import db 

def create_picture_details(picture_id, user_id, status):
    newPicDetails = Picture_Details(picture_id,user_id, status)
    db.session.add(newPicDetails)
    db.session.commit()
