from flask import Flask, render_template, redirect, request, abort
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
# Сделать загрузку фото
# Сделать изменение вакансий
# Сделать navbar
# Сделать просмотр профилей
# Добавить в поиск вакансий поиск компаний
# Сделать общую страницу ошибки (# страница ошибки)
# Сделать отправку письма при отклике

def post_message():
    pass


# Работает
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Работает
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
    elif data['search_btn'] and data['search'] != '':
        return redirect(f'/search/{data["search"]}')
    elif data['search_btn']:
        return render_template('base_page.html', title='Главная страница', form=form, error='Пустое поле ввода')
    return render_template('base_page.html', title='Главная страница', form=form)


# Работает
# Страница регистрации 
@app.route('/registration', methods=['GET', 'POST'])
def reg():
    form = registerForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация работодателя', \
                                   sec_title='Регистрация работодателя', error='Данный email уже занят', \
                                   form=form)
        if '@' not in form.email.data:
            return render_template('registration.html', title='Регистрация работодателя', \
                                   sec_title='Регистрация работодателя', error='Неправильный формат почты', \
                                   form=form)

        user = User(login=form.login.data,
                    name=form.name.data,
                    description=form.description.data,
                    email=form.email.data,
                    telephone=form.telephone.data,
                    is_employer=form.is_employer.data, )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        login_user(user, remember=form.remember_me.data)

        return redirect('/')

    return render_template('registration.html', title='Регистрация', \
                           sec_title='Регистрация', form=form)


# Работает
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


# Работает
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = LoginForm()
    if current_user.is_employer:
        all_vac = current_user.vacancy
    else:
        s = current_user.responded_vacancies
        all_vac = []
        if s != '':
            ids = [int(x) for x in s.split(';')]
            db_sess = db_session.create_session()
            all_vac = db_sess.query(Vacancy).filter(Vacancy.id.in_(ids))
    return render_template('profile.html', title='Личный кабинет', sec_title='Личный кабинет', form=form,
                           sp=all_vac)


# Работает
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Не работает
@app.route('/change_profile/<name>', methods=['GET', 'POST'])
@login_required
def change_profile(name):
    pass
    # Сделать проверку на пользователя current_user.name == name
    return 'заглушккккккккк change_profile'


# Работает
@app.route('/new_vacancy', methods=['GET', 'POST'])
@login_required
def new_vacancy():
    form = NewVacancy()
    if form.validate_on_submit():
        if not current_user.is_employer:
            return 'Вы не являетесь работодателем!'
        vacancy = Vacancy(title=form.title.data, content=form.content.data)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.vacancy.append(vacancy)
        db_sess.commit()
        return redirect('/profile')
    return render_template('new_vacancy.html', form=form, title='Добавление вакансии', sec_title='Добавление вакансии')


# Работает
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
    # страница ошибки
    return 'Недостаточно прав!'


# Работает
@app.route('/remove_vacancy/<id>', methods=['POST', 'GET'])
@login_required
def delete_vacancy(id):
    db_sess = db_session.create_session()
    vacancy = db_sess.query(Vacancy).filter(Vacancy.id == id).first()
    if vacancy:
        if current_user.id == vacancy.user.id:
            db_sess.delete(vacancy)
            db_sess.commit()
            return redirect('/profile')
        elif f'{id}' in current_user.responded_vacancies:
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            s = user.responded_vacancies
            if f';{id}' in s:
                s = s.replace(f';{id}', '', 1)
            elif f'{id};' in s:
                s = s.replace(f'{id};', '', 1)
            else:
                s = s.replace(f'{id}', '', 1)
            user.responded_vacancies = s
            db_sess.commit()
            return redirect('/profile')
        else:
            return 'Недостаточно прав!'
    else:
        abort(404)


# Работает
@app.route('/change_vacancy/<id>', methods=['GET', 'POST'])
@login_required
def change_vacancy(id):
    form = NewVacancy()
    if request.method == "GET":
        db_sess = db_session.create_session()
        vacancy = db_sess.query(Vacancy).filter(Vacancy.id == id, Vacancy.user == current_user).first()
        if vacancy:
            if current_user.id == vacancy.user.id and vacancy.user.is_employer:
                form.title.data = vacancy.title
                form.content.data = vacancy.content
            else:
                # страница ошибки
                return 'Вы не являетесь создателем новости'
        else:
            # страница ошибки
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        vacancy = db_sess.query(Vacancy).filter(Vacancy.id == id, Vacancy.user == current_user).first()
        if vacancy:
            if current_user.id == vacancy.user.id and vacancy.user.is_employer:
                vacancy.title = form.title.data
                vacancy.content = form.content.data
                db_sess.commit()
                return redirect('/profile')
            # страница ошибки
            return 'Вы не являетесь создателем новости'
        else:
            # страница ошибки
            abort(404)
    return render_template('change_vacancy.html',
                           title='Редактирование вакансии',
                           sec_title='Редактирование вакансии',
                           form=form
                           )


@app.route('/respond_vacancy/<id>', methods=['GET', 'POST'])
@login_required
def respond_vacancy(id):
    form = respond_Form()
    if request.method == "GET":
        if not current_user.is_employer:
            db_sess = db_session.create_session()
            vacancy = db_sess.query(Vacancy).filter(Vacancy.id == id).first()
            if vacancy:
                vacancies = db_sess.query(Vacancy).filter(Vacancy.company_id == current_user.id).all()
                if vacancy in vacancies:
                    # страница ошибки
                    return 'Вы уже откликнулись на эту вакансию'

                return render_template("respond_vacancy.html", title='Отклик на вакансию',
                                       sec_title='Отклик на вакансию', form=form)
            else:
                # страница ошибки
                abort(404)
        else:
            # страница ошибки
            return 'Вы не являетесь сотрудником'
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(current_user.id == User.id).first()
        s = user.responded_vacancies
        if s != '':
            s += f';{id}'
        else:
            s = str(id)
        user.responded_vacancies = s
        db_sess.commit()
        return redirect('/profile')
    return render_template("respond_vacancy.html", title='Отклик на вакансию',
                           sec_title='Отклик на вакансию', form=form)


@app.route('/search/<text>', methods=['GET', 'POST'])
def search(text):
    db_sess = db_session.create_session()
    vacancies = db_sess.query(Vacancy).filter(
        (Vacancy.content.like(f'%{text}%')) | (Vacancy.title.like(f'%{text}%'))).all()
    return render_template('search.html', sp=vacancies, title='Поиск', sec_title=f'Все вакансии по запросу "{text}"')


if __name__ == '__main__':
    db_session.global_init("db/info.db")
    app.run(port=8080, host='127.0.0.1')
