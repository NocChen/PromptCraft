## app/models.py
from datetime import datetime
from app import db, bcrypt
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    documents = db.relationship('Document', backref='author', lazy=True)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    commits = db.relationship('Commit', backref='document', lazy=True)

    def __init__(self, title: str, content: str, owner: User):
        self.title = title
        self.content = content
        self.user_id = owner.id

class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)

    def __init__(self, message: str, document: Document):
        self.message = message
        self.document_id = document.id
