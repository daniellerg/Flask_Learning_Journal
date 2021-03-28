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
@login_required
def index():
    stream = models.Entry.select().limit(25).order_by(models.Entry.entry_date)
    render_template('index.html', stream=stream)


@app.route('/entries/new', methods=('GET', 'POST'))
@login_required
def create():
    form = forms.EntryForm()
    if form.validate_on_submit():
        try:
            models.Entry.create_entry(
                title=form.title.data,
                entry_date=form.entry_date.data,
                time_spent=form.time_spent.data,
                learned=form.learned.data,
                resources=form.resources.data,
                user=g.user.get_current_object()
            )
            return redirect(url_for('index'))
        except IntegrityError:
            pass
    return render_template('new.html', form=form)


@app.route('/entries/<int:entry_id>', methods=('GET', 'POST'))
@login_required
def detail(entry_id):
    try:
        entry = models.Entry.select().where(models.Entry.entry_id==entry_id)
        return render_template('detail.html', entry=entry)
    except DoesNotExist:
        abort(404)
    return render_template('index.html')


@app.route('/entries/<int:entry_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(entry_id):
    updated_entry = models.Entry.get(models.Entry.entry_id==entry_id)
    updated_entry


@app.route('/entries/<int:entry_id>/delete', methods=('GET', 'POST'))
@login_required
def delete(entry_id):
    try:
        models.Entry.get(entry_id).delete_instance()
    except models.IntegrityError:
        pass
    else:
        flash('Entry deleted.', 'success')
    return render_template('index.html')


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
            title='Hello', 
            entry_date='03/27/2021', 
            time_spent=5, 
            learned='python', 
            resources='python',
            user=current_user
            )
    except ValueError:
        pass
    app.run(debug=True, port=8000, host='localhost')

