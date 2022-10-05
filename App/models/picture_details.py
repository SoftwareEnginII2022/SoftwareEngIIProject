from App.database import db
from enum import Enum

class Status (Enum):
    Like = "Like"
    Dislike = "Dislike"


class Picture_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture_id = db.Column(db.Integer,db.ForeignKey('picture.id'), nullable= False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable= False)
    status = db.Column (db.Enum(Status), nullable = False)

    def __init__(self,picture_id, user_id):
        self.picture_id = picture_id
        self.user_id = user_id

    def like(self):
        self.status = Status.Like

    def dislike(self):
        self.status = Status.Dislike
        
    def toJSON(self):
        return {
            'id':self.id,
            'picture_id':self.picture_id,
            'user_id': self.user_id,
            'Status': self.status.name
        }
    
        

   
