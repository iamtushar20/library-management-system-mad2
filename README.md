# Library Management System (Frontend & Backend)

## Description
The **Library Management System** is a full-stack web application designed to manage an online library. The system provides functionality for both **administrators** and **users**. Administrators can manage books and sections through CRUD operations, while users can browse, read, request, or purchase books. The application supports authentication, user management, and search functionality.

---

## Features

### User Features
- Register, log in, log out, and manage user profiles.
- Browse available sections and books.
- Request or purchase books.
- View issued books and transaction history.
- Return books and provide feedback.
- Search books by name, author, or section.

### Admin Features
- Perform CRUD operations on sections and books.
- Manage book requests by approving, denying, or revoking access.
- View all books, sections, requests, and feedback.
- Access an admin dashboard with analytics and insights.

---

## Technologies Used

### Backend
- **Flask** – Python web framework for handling routing and backend logic.
- **Flask-SQLAlchemy** – ORM for managing the database and relationships.
- **Celery** – Asynchronous task queue for background operations.
- **Redis** – In-memory data store used as a message broker with Celery.

### Frontend
- **Vue.js 3** – JavaScript framework for building reactive and dynamic interfaces.
- **Bootstrap** – For responsive design and styling of UI components.
- **JavaScript (ES6)** – Client-side scripting and interactivity.
- **Vite CLI** – Development tool for efficient frontend builds.

### Other Tools
- **Node.js** – JavaScript runtime for dependency management.
- **npm** – Node package manager for managing project dependencies.

---

## Database Schema Design

### User Table
- Contains user information such as username, password, name, and admin status.
- Each user can request or purchase books.

### Section Table
- Represents different sections in the library.
- Fields: ID, name, creation date, and description.

### Book Table
- Contains book information including name, author, content, date added, price, and section association.

### BookTransaction Table
- Represents transactions between users and books.
- Includes fields such as request date, issue date, return date, status, and feedback.
- Linked to both `User` and `Book` tables via foreign keys.

---

## Architecture Overview

### Backend
- `app.py`: Initializes the Flask application, database, and imports routes.
- `models.py`: Defines database models and relationships.
- `routes.py`: Handles route definitions and backend logic for user and admin operations.

### Frontend
- Developed using Vue.js 3 and Bootstrap.
- Communicates with the Flask backend via RESTful APIs.
- Uses Vite CLI for project setup and build optimization.

---

## Search Functionality
The search feature allows both administrators and users to search for books using:
- Section name
- Book name
- Author name

---

## Demo Video
Watch the demonstration of the project here:  
[https://youtu.be/Tg37XV8n7bU](https://youtu.be/Tg37XV8n7bU)

---

## Folder Structure

