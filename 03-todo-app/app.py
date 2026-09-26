from flask import Flask,render_template,request,redirect,url_for
app=Flask(__name__)

tasks=[]

@app.route("/" ,methods=['GET','POST'])
def home():
    if request.method=="POST":
        task=request.form["task"].strip()
        if task:
            new_task={
            "title":task,
            "completed":False
            }
            tasks.append(new_task)
            return redirect(url_for("home"))
    return render_template("index.html",tasks=tasks)


@app.route("/complete/<int:task_id>",methods=["POST"])
def completed_task(task_id):
    tasks[task_id]["completed"]=True
    
    return redirect(url_for("home"))



@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    tasks.pop(task_id)

    return redirect(url_for("home"))
