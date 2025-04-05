from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime as dt

from data import db_session
from data.users import User
from data.vacancies import Vacancy
from forms.login import LoginForm

from forms.all_forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'piggydoggy??piggydoggy'

login_manager = LoginManager()
login_manager.init_app(app)


# Повторить пароль в форме регистрации
# Сделать поиск вакансий
# Сделать отклики на вакансии
# Сделать navbar


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def default_page():
    form = base_page()
    data = form.data
    if data['registration']:
        return redirect('/registration')
    elif data['login']:
        return redirect('/login')
    elif data['logout_btn']:
        return redirect('/logout')
    elif data['profile_btn']:
        return redirect('/profile')

    return render_template('base_page.html', title='Главная страница', form=form)


# Страница регистрации работодателя
@app.route('/registration', methods=['GET', 'POST'])
def reg():
    form = registerForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        # ПРОВЕРКА ПО ДАННЫМ В БД !!!!!!!!!!!!!!!!!
        # if db_sess.query(Company).filter(Company.email == form.company_email.data).first() or \
        #         db_sess.query(User).filter(User.email == form.company_email.data).first():
        #     return render_template('registration.html', title='Регистрация работодателя', \
        #                            sec_title='Регистрация работодателя', error='Данный email уже занят', \
        #                            form=form)
        print(form.data)
        user = User(login=form.login.data,
                    name=form.name.data,
                    description=form.description.data,
                    email=form.email.data,
                    telephone=form.telephone.data,
                    is_employer=form.is_employer.data, )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('registration.html', title='Регистрация', \
                           sec_title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            print(123)
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Авторизация', sec_title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', sec_title='Авторизация', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = LoginForm()
    all_vac = current_user.vacancy
    return render_template('profile.html', title='Личный кабинет', sec_title='Личный кабинет', form=form,
                           sp=all_vac)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/change_profile/<name>', methods=['GET', 'POST'])
@login_required
def change_profile(name):
    pass
    # Сделать проверку на пользователя current_user.name == name
    return 'заглушккккккккк change_profile'


@app.route('/new_vacancy', methods=['GET', 'POST'])
@login_required
def new_vacancy():
    form = NewVacancy()
    if form.validate_on_submit():
        if not current_user.is_employer:
            return render_template('new_vacancy.html', form=form, title='Добавление вакансии',
                                   sec_title='Добавление вакансии', error='Вы не являетесь работодателем!')
        vacancy = Vacancy(title=form.title.data, content=form.content.data)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.vacancy.append(vacancy)
        db_sess.commit()
        return redirect('/profile')
    return render_template('new_vacancy.html', form=form, title='Добавление вакансии', sec_title='Добавление вакансии')


@app.route('/remove_profile/<id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    pass
    db_sess = db_session.create_session()

    if current_user.id == int(id):
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        logout_user()
        vacancy = user.vacancy
        for el in vacancy:
            db_sess.delete(el)
        db_sess.delete(user)
        db_sess.commit()
        return redirect('/')
    return 'Недостаточно прав!'


@app.route('/remove_vacancy/<id>', methods=['POST', 'GET'])
@login_required
def delete_vacancy(id):
    db_sess = db_session.create_session()
    vacancy = db_sess.query(Vacancy).filter(Vacancy.id == id).first()
    if current_user.is_employer and current_user.id == vacancy.user.id:
        print(vacancy)
        db_sess.delete(vacancy)
        db_sess.commit()
        return redirect('/profile')
    return 'Недостаточно прав!'




@app.route('/change_vacancy/<id>', methods=['GET', 'POST'])
@login_required
def change_vacancy(id):
    # Сделать проверку на пользователя
    return 'заглушккккккккк change_vacancy'


if __name__ == '__main__':
    db_session.global_init("db/info.db")
    # db_sess = db_session.create_session()
    # user = db_sess.query(User).filter(User.id == 1).first()
    # vacancy = Vacancy(title="Программист", content="Пишем программы")
    # user.vacancy.append(vacancy)
    # db_sess.commit()

    app.run(port=8080, host='127.0.0.1')
