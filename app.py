from curses import echo
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # create a new instance of Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # connect to database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # do not track modifications
db = SQLAlchemy(app)  # create a new instance of SQLAlchemy


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Todo %r>" % self.id


@app.route("/", methods=["GET", "POST"])  # routeto display all todos
def index():
    if request.method == "POST":
        content = request.form["content"]
        task_content = Todo(content=content)  # create a new todo item
        try:
            db.session.add(task_content)
            db.session.commit()  # add the new todo item to the database
            return redirect("/")
        except:
            return "There was an issue adding your task"

    if request.method == "GET":
        tasks = Todo.query.order_by(Todo.date_created).all()
        print(tasks)
        return render_template("index.html", tasks=tasks)  # render the index.html page
    else:
        print("inside else")
    return render_template("index.html")


@app.route("/delete/<int:id>", methods=["GET", "POST", "DELETE"])
def index2(id):
    task_to_delete = Todo.query.get_or_404(id)
    print(task_to_delete)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def index3(id):

    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        task_to_update.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task"
    if request.method == "GET":
        task = Todo.query.get_or_404(id)
        return render_template("update.html", task=task)
    else:
        return render_template("update.html", task_to_update=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)  # run the app in debug mode on port 5000
