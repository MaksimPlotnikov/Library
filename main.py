from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.user import RegisterForm, LoginForm, BookForm
from forms.review import ReviewForm
from data.reviews import Reviews

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/book_1', methods=['GET', 'POST'])
def book_1():
    form = BookForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template('book_1.html', form=form)


@app.route('/book_2', methods=['GET', 'POST'])
def book_2():
    form = BookForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template('book_2.html', form=form)


@app.route('/book_3', methods=['GET', 'POST'])
def book_3():
    form = BookForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template('book_3.html', form=form)


def create_users():
    capitane = User()
    capitane.surname = 'Scott'
    capitane.name = 'Ridley'
    capitane.email = 'scott_chief@mars.org'

    db_sess = db_session.create_session()
    db_sess.add(capitane)
    db_sess.commit()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/reviews',  methods=['GET', 'POST'])
def all_reviews():
    db_sess = db_session.create_session()
    review = db_sess.query(Reviews)
    return render_template("reviews.html", reviews=review)


@app.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_reviews():
    form = ReviewForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        review = Reviews()
        review.title = form.title.data
        review.content = form.content.data
        db_sess.add(review)
        db_sess.commit()
        return redirect('/reviews')
    return render_template('add_review.html', title='Добавление отзыва',
                           form=form)


def main():
    db_session.global_init("db/books.db")
    app.run()


if __name__ == '__main__':
    main()