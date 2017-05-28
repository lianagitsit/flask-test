from flask import Flask, render_template, redirect, url_for, session, escape, request
app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        # return 'Logged in as %s' % escape(session['username'])
        return render_template('welcome.html', name=escape(session['username']))
    return render_template('index.html')

@app.route('/pretty')
def pretty():
    return 'We pretty.'

@app.route('/user/<username>')
def show_user_profile(username):
    if (username == "eric"):
        food = "orange chicken"
    else:
        food = "pre-chewed gum"
    return 'My favorite food is %s' % food

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/ugly')
def ugly():
    return redirect(url_for('pretty'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Za98j/3yX R~XHH!jmN]LWX/,?RT'