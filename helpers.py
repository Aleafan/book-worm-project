import random

from cs50 import SQL
from flask import redirect, session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bookworm.db")


# Decorate routes to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Generate random quote
def gen_random_quote():
    quotes_count = db.execute("SELECT COUNT(*) FROM quotes_default")[0]['COUNT(*)']
    random_id = random.randint(1, quotes_count)
    quote = db.execute("SELECT * FROM quotes_default WHERE id=?", random_id)[0]
    return quote

# Generate random book
def gen_random_book():
    books_count = db.execute("SELECT COUNT(*) FROM reading_list WHERE user_id=?", session['user_id'])[0]['COUNT(*)']
    if books_count == 0:
        return ''
    random_id = random.randint(0, books_count - 1)
    book = db.execute("SELECT * FROM reading_list WHERE user_id=?", session['user_id'])[random_id]
    return book