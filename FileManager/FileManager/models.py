from FileManager import db
from flask_login import UserMixin
import bcrypt

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def check_password(self, password):
        if bcrypt.checkpw(password.encode('utf-8'), self.password_hash):
            return True
        return False

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    sha256 = db.Column(db.String(64), nullable=False)
    path = db.Column(db.String(300), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
