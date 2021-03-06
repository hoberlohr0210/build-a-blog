from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:12345@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'iwillnevertell'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    new_post = db.Column(db.String(1000))
    completed = db.Column(db.Boolean)

    def __init__(self, title, new_post):
        self.title = title
        self.new_post = new_post
        self.completed = False
        
@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == "GET":
        return render_template('newpost.html')

    title_error = ''
    new_post_error = ''

    if request.method=="POST":
        title = request.form['title']
        new_post = request.form['new_post']

    if not title:
        title_error = "You left the title empty, you big goon!"
            

    if not new_post:
        new_post_error = "Whoops! You left the textbox blank!"
            
        
    if not title_error and not new_post_error:
        new_blog = Blog(title, new_post) 
        db.session.add(new_blog)
        db.session.commit()

        return redirect('/blog?id=' + str(new_blog.id))
                
    return render_template('newpost.html', title_error=title_error, new_post_error=new_post_error)    

@app.route('/blog', methods=['GET'])
def blog():

    if request.args:
        id = request.args.get("id")
        blog = Blog.query.get(id)
        
        return render_template('uniqueblog.html', title="Build a Blog", blog=blog)

    else:
        blogs = Blog.query.all()

        return render_template('blog.html', blogs=blogs)


if __name__ == '__main__':
    app.run()