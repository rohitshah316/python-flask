from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///blog.db"

db=SQLAlchemy(app)

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text,nullable=False)


with app.app_context():
    db.create_all()
    
  
    
@app.route("/")
def home():
    posts=Post.query.all()
    return render_template("index.html",posts=posts)


@app.route("/create",methods=["GET","POST"])
def create_post():
    if request.method=="POST":
        title=request.form["title"].strip()
        content=request.form["content"].strip()
        
        if title and content:
            post=Post(
                title=title,
                content=content
            )
            db.session.add(post)
            db.session.commit()
            
            return redirect(url_for("home"))
    
    return render_template("create.html")


@app.route("/post/<int:post_id>")
def view_post(post_id):
    post=Post.query.get_or_404(post_id)
    
    return render_template("post.html",post=post)


@app.route("/post/<int:post_id>/edit",methods=["GET","POST"])
def edit_post(post_id):
    post=Post.query.get_or_404(post_id)
    
    if request.method=="POST":
        post.title=request.form['title'].strip()
        post.content=request.form['content'].strip()
        
        if post.title and post.content:
            db.session.commit()
            
            return redirect(url_for("view_post",post_id=post.id))
        
    return render_template("edit.html",post=post)


@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("home"))
