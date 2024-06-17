from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, unique=True, nullable=False)
    chat_id = db.Column(db.BigInteger, unique=True, nullable=False)
    full_name = db.Column(db.String(20), unique=False, nullable=True)
    user_name = db.Column(db.String(20), unique=False, nullable=True)