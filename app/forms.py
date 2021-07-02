from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField("Correo Electronico", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Ingresar")


class SignupForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    email = EmailField("Correo Electronico", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Registrar")


class TodoForm(FlaskForm):
    description = StringField("Descripción", validators=[DataRequired()])
    submit = SubmitField("Crear")


class DeleteTodoForm(FlaskForm):
    submit = SubmitField("Borrar")


class UpdateTodoForm(FlaskForm):
    submit = SubmitField("Actualizar")
