from flask import Flask,render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'ec0241749a3aeeedd5e742a3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80), unique = True)
    subtitle = db.Column(db.String(120), unique = True)
    author = db.Column(db.String(30), unique = True)
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)



@app.route('/')
@app.route('/index')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html',post=post)


@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost',methods=['POST'])
def addpost():
    title = request.form.get("title", False)
    subtitle = request.form.get("subtitle", False)
    author = request.form.get("author", False)
    content = request.form.get("content", False)
    
    post= Blogpost(title=title, subtitle=subtitle, author=author,content=content,date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()


    
    return redirect(url_for('index'))



if __name__ == 'main':
    app.run(debug=True)