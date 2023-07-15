from flask import Flask, render_template, request, redirect, url_for, session
import DatabaseManager

# Connect to Database
db = DatabaseManager.Database('blog')

app = Flask(__name__)
app.secret_key = "super secret key"


# main page (login)
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ""

    # check username and password
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # successful login
        if db.check_login(username, password):
            msg = 'Login Successful'
            # add logged user to session
            user_id = db.get_user_id(username)
            print("USER ID GOT: ", user_id)
            session['logged_in'] = True
            session['username'] = username
            session['id'] = user_id
            return redirect(url_for('my_articles'))

        else:
            msg = 'Login Failed'

    return render_template('index.html', msg=msg)


# logout page
@app.route('/logout')
def logout():
    # remove user from session
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('login'))


# register page (register)
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ""
    # check username and password
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check existence of username and email
        if db.check_username(username):
            msg = 'Username already exists'
        elif db.check_email(email):
            msg = 'Email already exists'
        else:
            db.register(username, password, email)
            msg = 'User registered successfully'
    elif request.method == 'POST':
        msg = 'Please fill out the form correctly'

    return render_template('register.html', msg=msg)


@app.route('/my_articles')
def my_articles():
    # Check if user is logged in
    if 'logged_in' in session:
        username = session['username']
        user_id = session['id']
        print("USERID  ", user_id)
        print("USERNAME  ", username)
        articles = db.get_user_articles(user_id)
        print("ARTICELS: ", articles)
        return render_template('my_articles.html', username=username, articles=articles)
    else:
        return redirect(url_for('login'))


@app.route('/create_article', methods=['GET', 'POST'])
def create_article():
    show_alert = False
    if request.method == 'POST' and 'title' in request.form and 'content' in request.form:
        # Create variables for easy access
        title = request.form['title']
        content = request.form['content']
        user_id = session['id']
        db.add_article(title, content, user_id)
        show_alert = True

    return render_template('create_article.html', show_alert=show_alert)


@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    show_alert = False
    if request.method == 'POST' and 'title' in request.form and 'content' in request.form:
        # Create variables for easy access
        title = request.form['title']
        content = request.form['content']
        db.update_article(article_id, title, content)
        show_alert = True

    return render_template('edit_article.html', article=db.get_article(article_id), show_alert=show_alert)


@app.route('/delete_article/<int:article_id>', methods=['GET', 'POST'])
def delete_article(article_id):
    db.delete_article(article_id)
    return redirect(url_for('my_articles'))


if __name__ == '__main__':
    app.run()
