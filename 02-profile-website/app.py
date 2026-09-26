from flask import Flask,render_template


app=Flask(__name__)

@app.route("/")
def home():
    name="Rohit"
    job="Python Developer"
    return render_template("home.html",name=name,job=job)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    project_list = [
        "Hello Flask",
        "Personal Profile Website",
        "To-Do App"
    ]
    return render_template("projects.html",projects=project_list)


@app.route("/skills")
def skills():
    skill_list=[
        "Python","Flask","HTML","CSS","Git"
    ]
    return render_template("skills.html",skills=skill_list)