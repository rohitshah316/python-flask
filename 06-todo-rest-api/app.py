from flask import Flask,request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Flask", "completed": False},
    {"id": 2, "title": "Build REST API", "completed": False}
]


@app.route("/api/tasks",methods=["GET"])
def get_tasks():
    return {"tasks":tasks}


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return {"error": "Task not found"}, 404


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data:
        return {"error": "Title is required"}, 400

    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": False
    }

    tasks.append(new_task)

    return new_task, 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data["title"]
            task["completed"] = data["completed"]
            return task

    return {"error": "Task not found"}, 404



@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}

    return {"error": "Task not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)
