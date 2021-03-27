from flask import (Flask, render_template, redirect, 
                    url_for, g, flash, abort)
from flask_login import (current_user, LoginManager, 
                        login_user, logout_user, login_required)
from flask_bcrypt import generate_password_hash, check_password_hash

import models
import forms


app = Flask(__name__)
app.secret_key = '#(SJ(DGKncn9ee#$#@dkduedj)%K'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    g.db = models.db
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('You have registered successfully!', 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
            except models.DoesNotExist:
                flash('Email or password does not match, please try again', 'error')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You are logged in!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Email or password does not match, please try again', 'error')
    return render_template('login.html', form=form)

 @app.route('/logout')      
 @login_required
 def logout():
     logout_user()
     flash('You logged out successfully.', 'success')
     return redirect(url_for('index')) 


@app.route('/')
@app.route('/entries')
def index():
    stream = models.JournalList.select().limit(25).order_by(models.Entry.date.desc())
    render_template('index.html', stream=stream)


@app.route('/entries/new', methods=('GET', 'POST'))
def create():
    pass


@app.route('/entries/<id>', methods=('GET', 'POST'))
def detail(id):
    pass


@app.route('/entries/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    pass


@app.route('/entries/<id>/delete', methods=('GET', 'POST'))
def delete(id):
    pass


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='danig',
            email='dfleharty@gmail.com',
            password='python',
            admin=True
        )
    except ValueError:
        pass
    try:
        models.Entry.create_entry(
            title='Hello', date='date', 
            time_spent=5, learned='python', 
            resources='python'
            )
    except ValueError:
        pass
    app.run(debug=True, port=8000, host='localhost')

