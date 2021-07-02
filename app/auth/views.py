from flask import render_template, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.forms import LoginForm, SignupForm

from . import auth
from app.firestore_service import get_user, user_put
from app.models import UserData, UserModel


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Ya estabas logueado")

        return redirect(url_for("index"))

    else:
        login_form = LoginForm()
        context = {"login_form": login_form}

        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data

            user_doc = get_user(email)

            if user_doc.to_dict() is not None:
                username = user_doc.to_dict()["username"]
            else:
                username = user_doc.to_dict()["username"]

            if user_doc.to_dict() is not None:
                password_from_db = user_doc.to_dict()["password"]

                if check_password_hash(password_from_db, password):
                    user_data = UserData(username, email, password)
                    user = UserModel(user_data)

                    login_user(user)

                    flash("Bienvenido de nuevo")

                    redirect(url_for("hello"))

                else:
                    flash("La información no coincide")

            else:
                flash("El usuario no existe")

            return redirect(url_for("index"))

        return render_template("login.html", **context)


@auth.route("signup", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm()

    context = {"signup_form": signup_form}

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data
        password = signup_form.password.data

        user_doc = get_user(email)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, email, password_hash)
            user_put(user_data)

            user = UserModel(user_data)

            login_user(user)

            flash("Bienvenido")

            return redirect(url_for("hello"))

        else:
            flash("El usuario ya existe")

    return render_template("signup.html", **context)


@auth.route("logout")
@login_required
def logout():
    logout_user()
    flash("Regresa pronto")

    return redirect(url_for("auth.login"))
