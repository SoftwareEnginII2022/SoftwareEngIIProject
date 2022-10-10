from App.database import db

class Rating_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rater_user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable= False)
    ratee_profile_id = db.Column(db.Integer,db.ForeignKey('profile.id'), nullable= False)
    rating = db.Column(db.Integer, nullable = False)

    def __init__(self,rater_user_id, ratee_profile_id, rating):
        self.rater_user_id = rater_user_id
        self.ratee_profile_id = ratee_profile_id
        self.rating = rating

    def toJSON(self):
        return{
            'id':self.id,
            'rater_user_id': self.rater_user_id,
            'ratee_profile_id':self.ratee_profile_id,
            'rating':self.rating
        }
        



