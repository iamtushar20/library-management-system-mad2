import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from io import StringIO
import csv
from datetime import datetime, timedelta
from celery_config import celery
from models import db, User, Section, Book, BookTransaction
# from celery.schedules import crontab
import csv
from flask import render_template_string



@celery.task
def generate_monthly_report():
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    users = User.query.filter_by(role='user').all()
    
    
    for user in users:
        books = BookTransaction.query.filter_by(user_name=user.username, status='accepted').all()
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Monthly Report</title>
        </head>
        <body>
            <h1>Monthly Report</h1>
            <p>Dear {{ username }},</p>
            {% if books | length == 0 %}
                <p>You have no books issued in the month of {{ current_month }} {{ current_year }}.</p>
            {% else %}
                <p>This is your monthly report for the month of {{ current_month }} {{ current_year }}.</p>
                <table>
                    <thead>
                        <tr>
                            <th>Book Name</th>
                            <th>Authors</th>
                            <th>Issue Date</th>
                            <th>Return Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for book in books %}
                        <tr>
                            <td>{{ book.book_name }}</td>
                            <td>{{ book.book_author }}</td>
                            <td>{{ book.request_date }}</td>
                            <td>{{ book.return_date }}</td>
                        </tr>
                        {% endfor %}        
                    </tbody>
                </table>
            {% endif %}
            <p>Thank you for using our service.</p>
        </body>
        </html>
        """

        html_content = render_template_string(
                html_template,
                username=user.name,
                current_month=current_month,
                current_year=current_year,
                books=books
            )
        send_email(user.email, html_content)

def send_email(to_email, html_content):
    from_email='library123@gmail.com'
    subject = 'Monthly Activity Report'

    msg=MIMEMultipart('alternative')
    msg['Subject']=subject
    msg['From']=from_email
    msg['To']=to_email
    
    part1 = MIMEText(html_content, 'html')
    msg.attach(part1)

    smtp_server = 'localhost'
    smtp_port = 1025

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(from_email,to_email,msg.as_string())

# export csv part
@celery.task
def export_book_details_as_csv():
    books = BookTransaction.query.filter_by(status='accepted').all()


    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['User Name','Book Name', 'Authors', 'Issue Date', 'Return Date'])

    for book in books:
        csv_writer.writerow([
            book.user_name,
            book.book_name,
            book.book_author,
            str(book.issue_date),
            str(book.return_date)

        ])

    base_dir = os.path.abspath(os.path.dirname(__name__))
    csv_file_path = os.path.join(base_dir,'csv/books_report.csv')

    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_buffer.getvalue())
    return csv_buffer.getvalue()


@celery.task
def send_daily_reminders():
    users = User.query.filter_by(role='user').all()
    now = datetime.now()
    upcoming_return_date = (now + timedelta(days=1)).date()  # Converting to date object
    
    for user in users:
        # Checking  if the user has a book with an approaching return date
        transactions = BookTransaction.query.filter_by(status='accepted', user_name=user.username).all()
        upcoming_due_books = []
        for book in transactions:
            if book.return_date and book.return_date <= upcoming_return_date:
                upcoming_due_books.append((book.book_name, book.return_date))
                
        
        if upcoming_due_books:
            send_alert(user, upcoming_due_books)

def send_alert(user, books_due):
    
    book_details = "<br>".join([f"{book_name}: {return_date}" for book_name, return_date in books_due])
    alert_message = (f"Dear {user.name},<br><br>You have the following books due soon:<br>{book_details}<br><br>"
                     "Please return them on time to avoid penalties.")
    send_email_remainder(user.email, alert_message)
    

def send_email_remainder(to_email, alert_message):
    from_email = 'dailyreminders@gmail.com'
    subject = 'Reminder: Upcoming Book Return Due Date'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    part1 = MIMEText(alert_message, 'html')
    msg.attach(part1)

    smtp_server = 'localhost'
    smtp_port = 1025

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(from_email, to_email, msg.as_string())
