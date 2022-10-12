from App.database import db
from datetime import date

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable = False, default= 0)
    tier = db.Column(db.Integer,nullable= False, default= 0)
    daily_views = db.Column(db.Integer,nullable= False, default= 0)
    first_view_date = db.Column(db.Date, nullable= False, default= date(1970,1,1))
    Picture = db.relationship('Picture', backref='profile', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self,user_id):
        self.user_id = user_id
    
    def get_tier(self):
        return ("Bronze", "Gold", "Platinum", "Diamond")[int(self.tier/100)]

    def toJSON(self):
        return {
            'id':self.id,
            'user_id': self.user_id,
            'rating': self.rating,
            'tier':self.get_tier(),
            "tier_points": self.tier,
            'daily_views':self.daily_views,
            'first_view_date':self.first_view_date,
            'Pictures': [p.toJSON() for p in self.Picture]
        } 