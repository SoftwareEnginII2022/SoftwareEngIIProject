from App.database import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True),
    user_id = db.Column(db.Integer,nullable= False),
    tier = db.Column(db.Integer,nullable= False),
    view_count = db.Column(db.Integer,nullable= False, default= 0),
    first_view_date = db.Column(db.Date, nullable= False),
    db.relationship('Picture', backref='profile', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self,user_id, tier, view_count, first_view_date):
        self.user_id = user_id
        self.tier = tier
        self.view_count = view_count
        self.first_view_date = first_view_date

    def toJSON(self):
        return {
            'user_id': self.user_id,
            'tier':self.tier,
            'view_count':self.view_count,
            'first_view_date':self.first_view_date
        } 