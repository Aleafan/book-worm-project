from cs50 import SQL
from flask import Flask, render_template, session, redirect, request, abort, flash, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import os
import sqlalchemy

from helpers import login_required, gen_random_quote, gen_random_book


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response

# Configure CS50 Library to use SQLite database
db = SQL('sqlite:///bookworm.db')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    username = db.execute('SELECT username FROM users WHERE id=?', session['user_id'])[0]['username']
    book_suggest = gen_random_book()

    if request.method == 'POST':
        error = None
        query = request.form.get('query')
        if not query:
            error = 'Search field is empty'

        if error is None:
            search = db.execute('SELECT title, author, date, cover FROM books WHERE user_id=? AND (title LIKE ("%" || ? || "%") OR author LIKE ("%" || ? || "%"))', session['user_id'], query, query)
            if not search:
                error = 'Search returned no results'
            else:
                return render_template('index.html', quote=gen_random_quote(), username=username, book=book_suggest, search=search, query=query)

        flash(error)

    return render_template('index.html', quote=gen_random_quote(), username=username, book=book_suggest)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        # Validate user's input
        name = request.form.get('name')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        error = None
        if not name:
            error = 'Username is required.'
        elif not password or not confirmation:
            error = 'Password is required.'
        elif password != confirmation:
            error = 'Password confirmation is incorrect.'
        else:
            coinciding_names = db.execute('SELECT username FROM users WHERE username=?', name)
            if len(coinciding_names) != 0:
                error = 'User {} is already registered.'.format(name)

        # Record user's data into database
        if error is None:
            password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            db.execute('INSERT INTO users (username, hash) VALUES (?, ?)', name, password_hash)
            flash('You\'ve successfully registered!')
            return redirect('/login')

        flash(error)

    return render_template('register.html', quote=gen_random_quote())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        name = request.form.get('name');
        password = request.form.get('password')
        error = None

        user = db.execute('SELECT * FROM users WHERE username=?', name)
        if not user:
            error = 'This username is not registered.'
        elif not check_password_hash(user[0]['hash'], password):
            error = 'This password is incorrect.'

        if error is None:
            session['user_id'] = user[0]['id']
            return redirect('/')

        flash(error)

    return render_template('login.html', quote=gen_random_quote())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/library')
@login_required
def library():
    books = db.execute('SELECT * FROM books WHERE user_id = ?', session['user_id'])
    return render_template('library.html', quote=gen_random_quote(), books=books)


@app.route('/library/book')
@login_required
def book_upd_page():
    title = request.args.get('title')
    book = db.execute('SELECT * FROM books WHERE user_id = ? AND title = ?', session['user_id'], title)[0]
    return render_template('bookpage.html', quote=gen_random_quote(), book=book)


@app.route('/library/edit', methods=['GET', 'POST'])
@login_required
def edit_book():
    titl = request.args.get('title')
    print(titl)
    if request.method == 'POST':
        error = None
        title_old = request.form.get('title-old')
        title_upd = request.form.get('title')
        if not title_upd:
            error = 'Please provide book\'s title'
        if title_upd != title_old:
            title_check = db.execute('SELECT * FROM books WHERE user_id = ? AND title = ?', session['user_id'], title_upd)
            if title_check:
                error = 'This book\'s title already exists in your library'
        author = request.form.get('author')
        if not author:
            error = 'Please provide book\'s author'
        date = request.form.get('date')
        description = request.form.get('description')
        ideas = request.form.get('ideas')
        quotes = request.form.get('quotes')
        cover = request.form.get('cover')

        if error is None:
            db.execute('UPDATE books SET user_id = ?, title = ?, author = ?, date = ?, description = ?, ideas = ?, quotes = ?, cover = ? WHERE title = ?', session['user_id'], title_upd, author, date, description, ideas, quotes, cover, title_old)
            flash('"{}": data edited'.format(title_upd))
            return redirect('/library/book?title={}'.format(title_upd))

        flash(error)
        return redirect('/library/edit?title={}'.format(title_old))

    title = request.args.get('title')
    book = db.execute('SELECT * FROM books WHERE user_id = ? AND title = ?', session['user_id'], title)[0]
    return render_template('edit-book.html', quote=gen_random_quote(), book=book)


@app.route('/library/delete')
@login_required
def book_delete():
    title = request.args.get('title')
    db.execute('DELETE FROM books WHERE user_id = ? AND title = ?', session['user_id'], title)
    flash('{} was successfully deleted from library'.format(title))
    return redirect('/library')


@app.route('/addbook', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        error = None
        title = request.form.get('title')
        if not title:
            error = 'Please provide book\'s title'
        title_check = db.execute('SELECT * FROM books WHERE user_id = ? AND title = ?', session['user_id'], title)
        if title_check:
            error = 'This book\'s already in your library'
        author = request.form.get('author')
        if not author:
            error = 'Please provide book\'s author'
        date = request.form.get('date')
        description = request.form.get('description')
        ideas = request.form.get('ideas')
        quotes = request.form.get('quotes')
        cover = request.form.get('cover')

        if error is None:
            db.execute('INSERT INTO books (user_id, title, author, date, description, ideas, quotes, cover) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', session['user_id'], title, author, date, description, ideas, quotes, cover)
            flash('"{}" saved in your Library'.format(title))
            return redirect('/library')

        flash(error)

    return render_template('addbook.html', quote=gen_random_quote())


@app.route('/reading-list', methods=['GET', 'POST'])
@login_required
def reading_list():
    if request.method == 'POST':
        error = None
        title = request.form.get('title')
        if not title:
            error = 'Please provide book\'s title'
        title_check = db.execute('SELECT * FROM reading_list WHERE user_id = ? AND title = ?', session['user_id'], title)
        if title_check:
            error = 'This book\'s already in your list'
        author = request.form.get('author')
        if not author:
            error = 'Please provide book\'s author'

        if error is None:
            db.execute('INSERT INTO reading_list (user_id, title, author) VALUES (?, ?, ?)', session['user_id'], title, author)
            flash('{} saved in your list'.format(title))
            return redirect('/reading-list')

        flash(error)

    books = db.execute('SELECT * FROM reading_list WHERE user_id=?', session['user_id'])
    return render_template('read-list.html', quote=gen_random_quote(), books=books)

@app.route('/reading-list/delete')
@login_required
def delete_from_list():
    title = request.args.get('title')
    result = db.execute('DELETE FROM reading_list WHERE user_id=? AND title=?', session['user_id'], title)
    if result == 1:
        return 'true'
    else:
        return 'false'

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)