from flask import Flask,render_template, redirect, url_for,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, InputRequired, Length, DataRequired
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user,current_user, UserMixin


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec0241749a3aeeedd5e742a3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))

class LoginForm(FlaskForm):
    username= StringField(label='Username', validators=[Length(min=2,max=30),DataRequired()])
    password = PasswordField(label='Password', validators= [Length(min=6)])
    remember = BooleanField(label = 'Remeber Me')


class RegisterForm(FlaskForm):
    email= StringField(label= "Email",validators=[Email(), DataRequired()])
    username= StringField(label='Username', validators=[Length(min=2,max=30),DataRequired()])
    password = PasswordField(label='Password', validators= [Length(min=6)])



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                return redirect(url_for('userview'))
        return "<h1>Invalid username or password<h1>"
        
        
    return render_template('login.html',form=form )


@app.route('/signup', methods=['GET','POST'])
def signup():
    form=RegisterForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username = form.username.data,
                        email = form.email.data,
                        password = password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('signup.html',form=form)


@app.route('/userview')
@login_required
def userview():
    return render_template('userview.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)
    
