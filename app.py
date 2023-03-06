import requests
import config

from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
#bcrypt is used to hash password
from flask_bcrypt import Bcrypt

app = Flask(__name__)

#setting up the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#connects to our table
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#to secure the session cookie we need to set a secret key
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#3 columns in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    liked_images = db.Column(db.String(80), nullable=True)
    saved_images = db.Column(db.String(80), nullable=True)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')
 
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

#setting the different routes
#returning the html pages in the templates folder
@app.route('/')
def home():
    return render_template('home.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user_name = current_user.username
    return render_template('dashbord.html', user_name = user_name)



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/browse')
def browse():
    categories = ['age', 'alone', 'amazing', 'anger', 'architecture', 'art', 'attitude', 'beauty', 'best', 'birthday', 'business', 'cartouch', 'change', 'communications', 'computers', 'cool', 'courage', 'dad', 'dating', 'death', 'design', 'dreams', 'education', 'environmental', 'equality', 'experience', 'failure', 'faith', 'family', 'famous', 'fear', 'fitness', 'food', 'forgiveness', 'freedom', 'friendship', 'funny', 'future', 'god', 'good', 'government', 'graduation', 'great', 'happiness', 'health', 'history', 'home', 'hope', 'humor', 'imagination', 'inspirational', 'intelligence', 'jealousy', 'knowledge', 'leadership', 'learning', 'legal', 'life', 'love', 'marriage', 'medical', 'men', 'mom', 'money', 'morning', 'movies', 'success']
    return render_template('browse.html', categories=categories)


@app.route('/bucket')
def bucket():
    api_key = config.API_KEY

    api_url = 'https://api.api-ninjas.com/v1/bucketlist'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        bucketlist = response.json()['item']
    else:
        bucketlist = ''
    return render_template('browse.html', bucketlist=bucketlist)

@app.route('/quote', methods=['GET', 'POST'])
def quote():

    api_key = config.API_KEY

    category=request.form.get('category')

    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        quote = response.json()[0]['quote']
        author = response.json()[0]['author']
    else:
        quote =''
        author=''
    return render_template('browse.html', quote=quote, author=author)


@app.route('/base')
def base():
    return render_template('base.html')


if __name__ == "__main__":
    app.run(debug=True)