from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False
db = SQLAlchemy(app)


class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100))
    task_done = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

@app.route('/')
def main():
    todo_list = Todo.query.all()
    return render_template("main.html", todo_list = todo_list)

@app.route('/add', methods=['POST'])
def add():
    task_name = request.form.get('task_name')
    new_task = Todo(task_name = task_name, task_done = False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("main"))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.task_done = not todo.task_done
    db.session.commit()
    return redirect(url_for("main"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run()