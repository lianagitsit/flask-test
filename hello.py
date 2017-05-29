from flask import Flask, render_template, redirect, url_for, session, escape, request
from flask_sqlalchemy import SQLAlchemy

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'my_database',
    'host': 'localhost',
    'port': '5432',
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lianamancini:n0w a butterfly*@localhost/yournewdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<Look I Am Printing Record %r>' % self.username


@app.route('/')
def index():
    print('hello')
    if 'username' in session:
        # return 'Logged in as %s' % escape(session['username'])
        # Show a list of users in the database
        userlist = User.query.all()
        return render_template('welcome.html', name=escape(session['username']), userlist=userlist)
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

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        # print ("These are the values you wish to submit to the database: ")
        # print(request.form['username'])
        # print(request.form['email'])
        newuser = User(request.form['username'], request.form['email'])
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('adduser.html')

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

