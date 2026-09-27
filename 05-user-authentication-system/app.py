from flask import Flask,render_template,request,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,UserMixin,login_user,current_user,login_required,logout_user

app=Flask(__name__)



app.config["SECRET_KEY"]="dev-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///users.db"

db=SQLAlchemy(app)

login_manager=LoginManager()

login_manager.init_app(app)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True, nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    role=db.Column(db.String(20),default="user",nullable=False)
    
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]
        
        existing_user=User.query.filter_by(username=username).first()
        
        if existing_user:
            return "Username already exists!"
        
        existing_email=User.query.filter_by(email=email).first()
        
        if existing_email:
            return "Email already exists!"
        
        hashed_password=generate_password_hash(password)
        
        user=User(
            username=username,
            email=email,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        
        return "Registration received!"
    
    return render_template("register.html")




@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        
        user=User.query.filter_by(username=username).first()
        
        if user is None:
            return "Username not found!"
        
        if not check_password_hash(user.password,password):
            return "Incorrect password!"
        
        login_user(user)
        
        return render_template("dashboard.html")
    
    return render_template("login.html")


@app.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        return "Access denied!", 403

    return "Welcome to the admin area!"



@app.route("/dashboard")
@login_required
def dashboard():
   
    return render_template("dashboard.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/logout")
def logout():
    logout_user()
    
    return redirect(url_for('login'))


if __name__=="__main__":
    app.run(debug=True)