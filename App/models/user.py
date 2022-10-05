from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(40), nullable= False)
    last_name = db.Column(db.String(40), nullable = False)
    db.relationship('Profile', backref='user', lazy=True, cascade="all, delete-orphan")
    Picture = db.relationship('Picture', backref='user', lazy=True, cascade="all, delete-orphan")
    db.relationship('Picture_Details', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name

    def toJSON(self):
        return{
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'pictures': [p.toJSON for p in self.Picture]
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

