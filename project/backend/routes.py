from flask import render_template, request, redirect, url_for, flash, session, Response, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps
from sqlalchemy import or_
from datetime import datetime, date
from sqlalchemy import func
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager, unset_jwt_cookies


from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_caching import Cache
import redis
import os




from app import app
api= Api(app)


redis_client = redis.Redis(host="localhost", port=6380, db=0)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client})
from models import *



def check_return_and_revoke(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        issues = BookTransaction.query.filter_by(status='accepted').all()

        
        for issue in issues:
            # Checking if current date is greater than return date
            if datetime.now().date() > issue.return_date:
                # Updating approved status to 'revoked'
                issue.status = 'revoked'
                # Updating return date to current date
                issue.return_date = datetime.now().date()
                # Commiting changes to the database
                db.session.commit()

        return func(*args, **kwargs)

    return wrapper


@app.route('/')

def home():
    return "Hello MAD 2"

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'Logged out successfully'})
    unset_jwt_cookies(response)
    return response, 200


class SignupResource(Resource):
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        
        
        if not name or not email or not username or not password:
            return {'error': 'All fields are required'}, 400
        if '@' not in email or '@' not in username:
            return {'error': 'Please add @ in username'}, 400

        if User.query.filter((User.username == username)).first():
            return {'error': 'Username already exists'}, 400

        if User.query.filter_by(email=email).first():
            return {'error': 'Email already associated with another user'}, 400

        user = User(name=name, email=email, username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201
    
class LoginResource(Resource):
    
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        # setting access_token

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity={
                'id': user.id, 'username': user.username, 'role': user.role
            })
            return {
                'message': 'Login successful',
                'access_token': access_token,
                'userRole': user.role
            }, 200

        return {'error': 'Invalid username or password'}, 401



class SectionResource(Resource):
    


    def get(self):
        sections = Section.query.all()
        sections_data = [
            {
                'id': section.id,
                'name': section.name,
                'date_created': section.date_created.strftime('%Y-%m-%d'),
                'description': section.description
            }
            for section in sections
        ]
        return jsonify(sections_data)
    
    def post(self):
        data = request.get_json()
        sectionname = data.get('sectionname')
        date_created = data.get('date_created')
        description = data.get('description')
        existing_section = Section.query.filter_by(name=sectionname).first()
        if existing_section:
            return {"message": "Section name already exists"}, 400

        date_created = datetime.strptime(date_created, '%Y-%m-%d').date()

        new_section = Section(name=sectionname, date_created=date_created, description=description)
        db.session.add(new_section)
        db.session.commit()

        return {"message": "Section added successfully"}, 201
    
class SectionEditResource(Resource):
    
    def get(self, section_id):
        section = Section.query.get(section_id)
        if section is None:
            return jsonify({'error': 'Section not found'}), 404
        
        section_data = {
            'id': section.id,
            'name': section.name,
            'date_created': section.date_created.strftime('%Y-%m-%d'),
            'description': section.description
        }
        return jsonify(section_data)

    def put(self, section_id):
        section = Section.query.get(section_id)
        if section is None:
            return jsonify({'error': 'Section not found'}), 404
        
        data = request.get_json()
        new_section_name = data.get('name', section.name)
        
        
        existing_section = Section.query.filter(Section.name == new_section_name, Section.id != section_id).first()
        if existing_section:
            return {'message': 'Section name already exists'}, 400
        section.name = data.get('name', section.name)
        
    
        date_created_str = data.get('date_created', section.date_created)
        if isinstance(date_created_str, str):
            try:
                section.date_created = datetime.strptime(date_created_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        else:
            section.date_created = date_created_str
        
        section.description = data.get('description', section.description)
        
        db.session.commit()
        return jsonify({'message': 'Section updated successfully'})
    
    def delete(self, section_id):
        section = Section.query.get(section_id)
        if section:
            
            books = Book.query.filter_by(section_id=section_id).all()

            for book in books:
                BookTransaction.query.filter_by(book_name=book.name).delete()
            
            Book.query.filter_by(section_id=section_id).delete()

            db.session.delete(section)
            db.session.commit()
            
            return {'message': 'Section and its books deleted successfully'}, 200
        else:
            return {'error': 'Section not found'}, 404
        



    
class SectionBooksResource(Resource):
    
    @cache.cached(timeout=2)     # Caching the response for 2 seconds to reduce database load for frequent requests
    def get(self, section_id):
        books = Book.query.filter_by(section_id=section_id).all()

        books_data = [
            {
                'id': book.id,
                'section_id': book.section_id,
                'name': book.name,
                'content': book.content,
                'authors': book.authors,
                'date_added': book.date_added.strftime('%Y-%m-%d'),
                'price': book.price
            }
            for book in books
        ]
        return jsonify(books_data)

class SectionUserResource(Resource):

    def get(self, section_id=None):
        if section_id:
            section = Section.query.get_or_404(section_id)
            books = Book.query.filter_by(section_id=section.id).all()
            books_data = [
                {
                    'id': book.id,
                    'name': book.name,
                    'content': book.content,
                    'authors': book.authors,
                    'date_added': book.date_added.strftime('%Y-%m-%d') if book.date_added else None,
                    'price': book.price
                } for book in books
            ]
            section_data = {
                'id': section.id,
                'name': section.name,
                'date_created': section.date_created.strftime('%Y-%m-%d'),
                'description': section.description,
                'books': books_data
            }
            return jsonify(section_data)
        else:
            sections = Section.query.all()
            sections_data = [
                {
                    'id': section.id,
                    'name': section.name,
                    'date_created': section.date_created.strftime('%Y-%m-%d'),
                    'description': section.description
                } for section in sections
            ]
            return jsonify(sections_data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        section = Section(name=args['name'], description=args['description'], date_created=date.today())
        db.session.add(section)
        db.session.commit()
        return section.id, 201

class BookUserResource(Resource):
    
    def get(self, book_id=None):
        if book_id:
            book = Book.query.get_or_404(book_id)
            book_data = {
                'id': book.id,
                'section_id': book.section_id,
                'name': book.name,
                'content': book.content,
                'authors': book.authors,
                'date_added': book.date_added.strftime('%Y-%m-%d') if book.date_added else None,
                'price': book.price
            }
            return jsonify(book_data)
        else:
            books = Book.query.all()
            books_data = [
                {
                    'id': book.id,
                    'section_id': book.section_id,
                    'name': book.name,
                    'content': book.content,
                    'authors': book.authors,
                    'date_added': book.date_added.strftime('%Y-%m-%d') if book.date_added else None,
                    'price': book.price
                } for book in books
            ]
            return jsonify(books_data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('section_id', type=int, required=True, help="Section ID cannot be blank!")
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
        parser.add_argument('content', type=str, required=True, help="Content cannot be blank!")
        parser.add_argument('authors', type=str, required=True, help="Authors cannot be blank!")
        parser.add_argument('price', type=int, required=True, help="Price cannot be blank!")
        args = parser.parse_args()

        existing_book = Book.query.filter_by(name=args['name']).first()
        if existing_book:
            return {'message': 'Book name already exists !'}, 400

        book = Book(section_id=args['section_id'], name=args['name'], content=args['content'], authors=args['authors'], date_added=date.today(), price=args['price'])
        db.session.add(book)
        db.session.commit()
        return book.id, 201
    

class BookRequestResource(Resource):
    
    def get(self):
        req_list = BookTransaction.query.all()
        reqlist_data = [
            {
                'id': req.id,
                'user_name': req.user_name,
                'book_name': req.book_name,
                'book_author': req.book_author,
                'request_date': req.request_date.strftime('%Y-%m-%d'),
                'return_date': req.return_date.strftime('%Y-%m-%d'),
                'status': req.status
            }
            for req in req_list
        ]
        return reqlist_data, 200  

    def post(self):
        data = request.get_json()
        user_name = data.get('user_name')
        book_name = data.get('book_name')
        req_date = data.get('request_date')
        ret_date = data.get('return_date')

        
        if not user_name or not book_name or not req_date or not ret_date:
            return {'error': 'Please fill all input fields'}, 400

        try:
            request_date = datetime.strptime(req_date, '%Y-%m-%d').date()
            return_date = datetime.strptime(ret_date, '%Y-%m-%d').date()
        except ValueError:
            return {'error': 'Invalid date format, should be YYYY-MM-DD'}, 400

        
        user = User.query.filter_by(username=user_name).first()
        if user is None:
            return {'error': 'User not found'}, 404

        current_date = datetime.now().date()

        if request_date < current_date:
            return {'error': 'Please enter a valid request date'}, 400

        if request_date > return_date:
            return {'error': 'Return date cannot be before request date'}, 400

        # Checking if the book request duration is more than 7 days
        if (return_date - request_date).days > 7:
            return {'error': 'Book cannot be requested for more than 7 days'}, 400

        # Checking if user has more than 5 books issued
        issued_books_count = BookTransaction.query.filter(
            BookTransaction.user_name == user_name,
            BookTransaction.status == 'accepted').count()
        
        pending_books_count = BookTransaction.query.filter(
            BookTransaction.user_name == user_name,
            BookTransaction.status == 'pending'
        ).count()
        total_counts = issued_books_count + pending_books_count

        if total_counts >= 5:
            return {
            'error': f'You already have issued {issued_books_count} books and have {pending_books_count} pending requests, so you cannot issue more than 5 at any point of time'
        }, 400
        

        # Checking if user has already requested this book
        existing_request = BookTransaction.query.filter_by(user_name=user_name, book_name=book_name).filter(
            BookTransaction.status.in_(['pending', 'accepted'])
        ).first()
        if existing_request:
            return {'error': 'You have already requested or issued this book'}, 400

        # Checking if book exists
        book = Book.query.filter_by(name=book_name).first()
        if book is None:
            return {'error': 'Book not found'}, 404

        # Checking if user has already issued this book
        book_issued_already = BookTransaction.query.filter(
            BookTransaction.user_name == user_name,
            BookTransaction.book_name == book_name,
            BookTransaction.status == 'accepted'
        ).first()
        if book_issued_already:
            return {'error': 'You have already issued this book'}, 400

        
        new_request = BookTransaction(
            user_name=user_name,
            book_name=book_name,
            book_author=data.get('book_author', ''),
            request_date=request_date,
            return_date=return_date,
            status='pending'
        )
        db.session.add(new_request)
        db.session.commit()

        return {'message': 'Book request submitted successfully!'}, 201
    
class BookRequestUpdateResource(Resource):
    
    def post(self, req_id):
        data = request.get_json()
        new_status=data.get('status')
        requested_book = BookTransaction.query.get(req_id)

        if not requested_book:
            return jsonify({'message': 'Book request not found!'}), 404
        

        if (new_status == 'accepted'):
            requested_book.status = 'accepted'
            today = date.today()
            requested_book.issue_date = today

        elif (new_status == 'rejected'):
            requested_book.status = 'rejected'

        elif (new_status == 'returned'):
            requested_book.status = 'returned'
            today = date.today()
            requested_book.return_date = today

        elif (new_status == 'cancelled'):
            requested_book.status = 'cancelled'

        else:
            requested_book.status = 'revoked'
            today = date.today()
            requested_book.return_date = today

        db.session.commit()

        return {'message':f'You have successfully {requested_book.status} {requested_book.book_name} book!', 'status': new_status }




        

    
class BookTransactionResource(Resource):
    
    def get(self, transaction_id=None):
        if transaction_id:
            transaction = BookTransaction.query.get_or_404(transaction_id)
            transaction_data = {
                'id': transaction.id,
                'user_name': transaction.user_name,
                'book_name': transaction.book_name,
                'request_date': transaction.request_date.strftime('%Y-%m-%d'),
                'return_date': transaction.return_date.strftime('%Y-%m-%d') if transaction.return_date else None,
                
                'status': transaction.status,
                'feedback': transaction.feedback
            }
            return jsonify(transaction_data)
        else:
            transactions = BookTransaction.query.all()
            transactions_data = [
                {
                    'id': t.id,
                    'user_name': t.user_name,
                    'book_name': t.book_name,
                    'request_date': t.request_date.strftime('%Y-%m-%d'),
                    'return_date': t.return_date.strftime('%Y-%m-%d') if t.return_date else None,
                    
                    'status': t.status,
                    'feedback': t.feedback
                } for t in transactions
            ]
            return jsonify(transactions_data)

    def post(self):
        data = request.json
        transaction = BookTransaction(
            user_name=data['user_name'],
            book_name=data['book_name'],
            request_date=date.today(),
            return_date=data.get('return_date'),
            status='pending'
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'id': transaction.id}), 201

class UserBookListFetchingResource(Resource):
    
    @cache.cached(timeout=2)    # Cache the response for 2 seconds to reduce database load for frequent requests
    def get(self):
        username = request.args.get('username')
        if username:
            
            requests = BookTransaction.query.filter_by(user_name=username).all()
        else:
            requests = BookTransaction.query.all()
        
        requests_data = [
            {
                'id': request.id,
                'user_name': request.user_name,
                'book_name': request.book_name,
                'book_author': request.book_author,
                'request_date': request.request_date.strftime('%Y-%m-%d'),
                'return_date': request.return_date.strftime('%Y-%m-%d'),
                'status': request.status,
                'issue_date': request.issue_date.strftime('%Y-%m-%d') if request.issue_date else None,
            }
            for request in requests
        ]
        return jsonify(requests_data)
    
api.add_resource(UserBookListFetchingResource, '/api/get/book_requests')

api.add_resource(BookTransactionResource, '/api/transactions', '/api/transactions/<int:transaction_id>')

api.add_resource(BookRequestResource, '/api/book_requests', '/api/get/book_requests')
api.add_resource(SectionUserResource, '/api/sections', '/api/sections/<int:section_id>')
api.add_resource(BookUserResource, '/api/books', '/api/books/<int:book_id>')

api.add_resource(BookRequestUpdateResource, '/book_requests/<int:req_id>/status')


    
api.add_resource(LoginResource, '/login')
api.add_resource(SignupResource, '/signup')
api.add_resource(SectionResource, '/addsection', '/sections')
api.add_resource(SectionEditResource, '/sections/<int:section_id>')

api.add_resource(SectionBooksResource, '/section/books/<int:section_id>')





class SearchBooks(Resource):
    
    def get(self):
        query = request.args.get('query', '').lower()
        if not query:
            return jsonify([])

        sections = Section.query.all()
        results = []
        for section in sections:
            books = Book.query.filter(
                db.or_(
                    Book.name.ilike(f'%{query}%'),
                    Book.authors.ilike(f'%{query}%')
                )
            ).all()
            if section.name.lower().find(query) != -1 or books:
                results.append({
                    'id': section.id,
                    'name': section.name,
                    'description': section.description,
                    'books': [{'id': book.id, 'name': book.name, 'authors': book.authors, 'content': book.content, 'date_added': book.date_added, 'price': book.price} for book in books]
                })

        return jsonify(results)

api.add_resource(SearchBooks, '/api/search')



@app.route('/api/admin/stats', methods=['GET'])

def get_admin_stats():
    total_users = User.query.count()
    total_sections = Section.query.count()
    total_books = Book.query.count()
    total_pending_requests = BookTransaction.query.filter_by(status='pending').count()
    total_issued_books = BookTransaction.query.filter_by(status='accepted').count()

    stats = {
        'total_users': total_users,
        'total_sections': total_sections,
        'total_books': total_books,
        'total_pending_requests': total_pending_requests,
        'total_issued_books': total_issued_books
    }

    return jsonify(stats)

@app.route('/api/admin/section_books', methods=['GET'])

def get_section_books():
    sections = Section.query.all()
    section_books = [{'section': section.name, 'book_count': len(section.books)} for section in sections]
    return jsonify(section_books)

@app.route('/api/admin/top_issued_books', methods=['GET'])

def get_top_issued_books():
    top_books = db.session.query(
        Book.name,
        func.count(BookTransaction.id).label('issue_count')
    ).join(BookTransaction, Book.name == BookTransaction.book_name)\
    .filter(BookTransaction.status.in_(['accepted', 'returned']))\
    .group_by(Book.name)\
    .order_by(func.count(BookTransaction.id).desc())\
    .limit(5).all()
    
    result = [{'name': book.name, 'issue_count': book.issue_count} for book in top_books]
    return jsonify(result)


def get_user_role():
    identity = get_jwt_identity()
    user = User.query.get(identity)
    if user:
        return user.role
    else:
        return None
    
class ExportResource(Resource):
    @jwt_required()
    def post(self):
       
        user_role = get_user_role()
        if user_role != 'admin':
            return {"message": "Access denied"}, 403
        try:
            from tasks import export_book_details_as_csv
            csv_data = export_book_details_as_csv()

            
            if not isinstance(csv_data, str):
                raise ValueError("CSV data is not a valid string")

            response = make_response(csv_data)
            response.headers['Content-Disposition'] = "attachment; filename=books_report.csv"
            response.headers['Content-type'] = 'text/csv'
            return response
        except Exception as e:
            
            return {'error': str(e)}, 500

api.add_resource(ExportResource, '/exportcsv')



class AllBookResource(Resource):
    
    def get(self):
        books = Book.query.all()
        books_data = [
            {
                'id': book.id,
                'section_id': book.section_id,
                'name': book.name,
                'content': book.content,
                'authors': book.authors,
                'date_added': book.date_added.strftime('%Y-%m-%d'),
                'price': book.price
            }
            for book in books
        ]
        return jsonify(books_data)

    def put(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        data = request.get_json()
        book.name = data.get('name', book.name)
        book.content = data.get('content', book.content)
        book.authors = data.get('authors', book.authors)
        book.date_added = datetime.strptime(data.get('date_added', book.date_added.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        book.price = data.get('price', book.price)

        db.session.commit()
        return jsonify({'message': 'Book updated successfully'}), 200

api.add_resource(AllBookResource, '/allbooks', '/allbooks/<int:book_id>')


class CRUDBookResource(Resource):
    
    def get(self, book_id=None):
        if book_id:
            book = Book.query.get(book_id)
            if not book:
                return {'error': 'Book not found'}, 404

            book_data = {
                'id': book.id,
                'section_id': book.section_id,
                'name': book.name,
                'content': book.content,
                'authors': book.authors,
                'date_added': book.date_added.strftime('%Y-%m-%d'),
                'price': book.price
            }
            return book_data, 200
        else:
            books = Book.query.all()
            books_data = [
                {
                    'id': book.id,
                    'section_id': book.section_id,
                    'name': book.name,
                    'content': book.content,
                    'authors': book.authors,
                    'date_added': book.date_added.strftime('%Y-%m-%d'),
                    'price': book.price
                }
                for book in books
            ]
            return books_data, 200

    def post(self):
        data = request.get_json()
        section_id = data.get('section_id')
        book_name = data.get('name')

        # Checking if a book with the same name already exists in the specified section
        existing_book = Book.query.filter_by(name=book_name).first()
        if existing_book:
            return {'error': 'Book name already exists !   '}, 400

        date = data['date_added']
        date = datetime.strptime(date, '%Y-%m-%d').date()
        new_book = Book(
            section_id=section_id,
            name=data['name'],
            content=data['content'],
            authors=data['authors'],
            date_added=date,
            price=data['price']
        )
        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book added successfully'}, 200

    def put(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        data = request.get_json()
        new_name = data.get('name', book.name)

        # Checking if a book with the same name already exists in the specified section and is not the current book
        existing_book = Book.query.filter(Book.name == new_name, Book.id != book_id).first()
        if existing_book:
            return {'message': 'Book name already exists !'}, 400
        
        book.name = data.get('name', book.name)
        book.content = data.get('content', book.content)
        book.authors = data.get('authors', book.authors)
        book.date_added = datetime.strptime(data.get('date_added', book.date_added.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        book.price = data.get('price', book.price)

        db.session.commit()
        return {'message': 'Book updated successfully'}, 200

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {'error': 'Book not found'}, 404
        
        
        BookTransaction.query.filter_by(book_name=book.name).delete()
        
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book and related transactions deleted successfully'}, 200


api.add_resource(CRUDBookResource, '/api/books', '/api/books/<int:book_id>')

import csv, io


def export_accepted_transactions():
    
    transactions = BookTransaction.query.filter_by(status='accepted').all()
    

    print(f"Number of accepted transactions: {len(transactions)}")
    for txn in transactions:
        print(f"Transaction - User: {txn.user_name}, Book: {txn.book_name}, Authors: {txn.book.authors}, Issue Date: {txn.issue_date}, Return Date: {txn.return_date}")

    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['User Name', 'Book Name', 'Authors', 'Issue Date', 'Return Date'])
    
    
    for txn in transactions:
        issue_date_str = txn.issue_date.strftime('%Y-%m-%d') if txn.issue_date else ''
        return_date_str = txn.return_date.strftime('%Y-%m-%d') if txn.return_date else ''
        
        writer.writerow([
            txn.user_name, 
            txn.book_name, 
            txn.book.authors, 
            str(txn.issue_date),
            str(txn.return_date)
        ])
    

    output.seek(0)
    
    
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=accepted_transactions.csv"
    response.headers["Content-type"] = "text/csv"
    return response

@app.route('/export_transactions')
def export_transactions():
    return export_accepted_transactions()



@app.route('/book_requests/<int:book_id>/feedback', methods=['POST'])


def submit_feedback(book_id):
    data = request.get_json()
    feedback = data.get('feedback')

    transaction = BookTransaction.query.filter_by(id=book_id).first()
    if transaction:
        transaction.feedback = feedback
        db.session.commit()
        return jsonify({'message': 'Feedback submitted successfully'}), 200
    else:
        return jsonify({'message': 'Book transaction not found'}), 404