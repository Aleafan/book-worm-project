# BookWorm web app

#### Video Demo: https://youtu.be/2dPtx8HbnQs

#### Introduction
BookWorm is a web application where users can catalogue books they read with summaries of key ideas, personal comments and favorite quotes.
Users also can store their lists of books to read in the future.
The app is intended to help summarize books' content and keep important personal ideas and thoughts for future reference.
This app is my final project for Harvard CS50's Introduction to Computer Science course.

#### Technologies
For back-end side of the project I used Flask web framework written in Python.
To store and access various data on the server I used SQLite database.
To store user log-in information from one request to the next I used Flask's Session object.
To secure users passwords on the server passwords are stored as hashes utilizing Werkzeug 1.0.1 library functionality.

For front-end side of the project I used HTML, CSS and JavaScript languages.
To simplify the development and get more experience I used Bootstrap framework.
jQuery library was also used to write AJAX requests to delete book from Reading list without refreshing whole page.

The project's directory contains:
- "application.py" file with Python code for web server;
- "helpers.py" file with helper functions for "application.py"
- "bookworm.db" file containing database with 4 tables: "users" (profiles data), "books" (library books data), "quotes\_default" (quotes for random quote generator), "reading\_list" (Reading list books data)
- "README.md" - project description
- "/templates" directory with html templates used to create final HTML file
- "/static" directory containing CSS file "styles.css" and directory with images

Versions:
- Flask 1.1.2
- Python 3.9.1
- SQLite version 3.34.0
- Bootstrap 5.0.0
- jQuery 3.5.1 (AJAX)

#### Scope of functionalities / Features
- the app was built with mobile-first approach, prioritizing responsiveness and accessibility
- app provides feedback to user actions using Flask's Message Flashing system
- register and log in to user's profile
- users passwords are stored on server hashed for security (using Werkzeug 1.0.1 library)
- random quote generator shows different quotes from database each time web page refreshes
- get book recommendations based on profile's Reading list
- search for books from profile's Library by title or author
- view books from user's Library, add new books, edit books' information, delete books
- provide url to cover images for books, default cover image is shown otherwise
- easily add and delete books in Reading list section (wish list of books to read)