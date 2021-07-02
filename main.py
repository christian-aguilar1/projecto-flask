from flask import (
    request,
    make_response,
    redirect,
    render_template,
    session,
    url_for,
    flash,
)
from flask_login import login_required, current_user

import unittest

from app import create_app
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
from app.firestore_service import get_todos, put_todo, delete_todo, update_todo

app = create_app()
app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = True


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html", error=error)


@app.route("/")
def index():
    user_ip = request.remote_addr

    response = make_response(redirect("/hello"))
    # response.set_cookie("user_ip", user_ip)
    session["user_ip"] = user_ip

    return response


@app.route("/hello", methods=["GET", "POST"])
@login_required
def hello():
    # user_ip = request.cookies.get("user_ip")
    user_ip = session.get("user_ip")
    email = current_user.id
    username = current_user.username
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    context = {
        "user_ip": user_ip,
        "todos": get_todos(user_id=email),
        "username": username,
        "todo_form": todo_form,
        "delete_form": delete_form,
        "update_form": update_form,
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=email, description=todo_form.description.data)

        flash("Tu tarea se creo con éxito!")

        return redirect(url_for("hello"))

    return render_template("hello.html", **context)


@app.route("/todos/delete/<todo_id>", methods=["GET", "POST"])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for("hello"))


@app.route("/todos/update/<todo_id>/<int:done>", methods=["GET", "POST"])
def update(todo_id, done):
    user_id = current_user.id

    update_todo(user_id=user_id, todo_id=todo_id, done=done)

    return redirect(url_for("hello"))


@app.route("/error")
def internal_server_error():
    return 1 / 0
