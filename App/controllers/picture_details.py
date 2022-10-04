from App.models import Picture_details
from App.database import db 

def create_picture_details(picture_id, user_id):
    newPicDetails = Picture_Details(picture_id,user_id)
    db.session.add(newPicDetails)
    db.commit()
