from App.database import db

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'), nullable= False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable = False)
    url = db.Column(db.String(255), nullable= False)
    likes = db.Column(db.Integer,nullable= False, default=0)
    dislikes = db.Column(db.Integer, nullable= False, default=0)
    db.relationship('Picture_Details', backref='picture', lazy=True, cascade="all, delete-orphan")

    def __init__(self, user_id, profile_id, url, likes, dislikes):
        self.user_id = user_id
        self.profile_id = profile_id
        self.url = url
        self.likes = likes
        self.dislikes = dislikes

    def toJSON(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'profile_id': self.profile_id,
            'url': self.url,
            'likes':self.likes,
            'dislikes':self.dislikes,
        }