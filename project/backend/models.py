from app import app

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager, unset_jwt_cookies
from functools import wraps
from datetime import datetime
from flask_restful import Resource, Api





app.app_context().push()

db = SQLAlchemy(app)
jwt = JWTManager(app)




# Defining SQLAlchemy models for  database schema

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable = False)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    role = db.Column(db.String(32), default='user', nullable=False)
    
  
    

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column (db.String(50), nullable=False, unique=True)
    date_created = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.String(255), nullable=False)  
    authors = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.Date)
    price = db.Column(db.Integer, nullable=False)
    
    section = db.relationship('Section', backref='books')


class BookTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    book_name = db.Column(db.String(255), db.ForeignKey('book.name'), nullable=False)
    book_author = db.Column(db.String(255), nullable=True)
    request_date = db.Column(db.Date, nullable=True)
    issue_date = db.Column(db.Date, nullable=True)
    return_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(255), default='pending', nullable=False)
    read = db.Column(db.String(255), nullable=True)
    feedback = db.Column(db.String(255), nullable=True)
    
    user = db.relationship('User', backref='book_transactions')
    book = db.relationship('Book', backref='book_transactions')
    
    
with app.app_context():
    db.create_all()

    admin_username = 'Library@123'
    admin_password = '11111'
    email = 'iamadmin20@gmail.com'
    role = 'admin'
    if not User.query.filter_by(username=admin_username).first():
        password_hash = generate_password_hash(admin_password)
        admin = User(name='Admin', email=email, username=admin_username, password=password_hash, role=role)
        db.session.add(admin)
        db.session.commit()


