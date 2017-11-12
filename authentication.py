from flask import jsonify, make_response, Blueprint, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from models import Student
from templates.template import LoginForm

auth = Blueprint('auth', __name__, url_prefix='/auth/v1')

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


@auth.route('/index', methods=['GET'])
def auth_student():
    """
    :return: возвращает имя студента, если он авторизован и "auth required" если пользователь неавторизован
    """
    if current_user.is_authenticated:
        return render_template(
            "index.html",
            title='Home',
            student=current_user
        )
    else:
        return make_response(
            jsonify(status="auth required"),
            401
        )


@auth.route('/login', methods=['GET', 'POST'])
def login_student():
    """
    Аутентификация пользователя
    :return:
    """
    form = LoginForm()
    good_password = '123'
    if current_user.is_authenticated:
        logout_user()

    if form.validate_on_submit():
        login = form.data["login"]
        password = form.data["password"]
        user = Student.query.get(int(login))
        if (user is None) or (password != good_password):
            return render_template('login_form.html', form=form)
        else:
            login_user(user)

            flash('Logged in successfully.')

            return redirect(url_for('.auth_student'))
    return render_template('login_form.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    Разлогинивает пользователя, удаляет куки из сессии
    :return:
    """
    logout_user()
    return redirect(url_for('.auth_student'))
