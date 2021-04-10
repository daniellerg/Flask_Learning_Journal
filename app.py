from flask import (Flask, render_template, redirect, 
                    url_for, g, flash, abort, request)
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
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    r_form = forms.RegisterForm()
    if r_form.validate_on_submit():
        models.User.create_user(
            username=r_form.username.data,
            email=r_form.email.data,
            password=r_form.password.data
            )
        flash('You have registered successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', r_form=r_form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == login_form.email.data)
        except models.DoesNotExist:
            flash('Email does not match, please try again', 'error')
        else:
            if check_password_hash(user.password, login_form.password.data):
                login_user(user)
                flash('You are logged in!', 'success')
                return redirect(url_for('index'))
            else:
                flash(
                    'Email or password does not match, please try again', 
                    'error')
    return render_template('login.html', login_form=login_form)


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
    return render_template('index.html', stream=stream)


@app.route('/entries/new', methods=('GET', 'POST'))
@login_required
def new_entry():
    entry_form = forms.EntryForm()
    if entry_form.validate_on_submit():
        models.Entry.create_entry(
            user=g.user._get_current_object(),
            title=entry_form.title.data,
            entry_date=entry_form.entry_date.data,
            time_spent=entry_form.time_spent.data,
            learned=entry_form.learned.data,
            resources=entry_form.resources.data,
            )
        flash('Entry posted!', 'success')
        return redirect(url_for('index'))
    return render_template('new.html', entry_form=entry_form)


@app.route('/entries/<int:entry_id>', methods=('GET', 'POST'))
@login_required
def detail(entry_id):
    try:
        entry = models.Entry.get(models.Entry.id==entry_id)
        return render_template('detail.html', entry=entry)
    except models.DoesNotExist:
        abort(404)
    return render_template('index.html')


@app.route('/entries/<int:entry_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(entry_id):
    try:
        updated_entry = models.Entry.get(models.Entry.id==entry_id)
    except models.DoesNotExist:
        abort(404)
    updated_form = forms.EntryForm()
    if current_user == updated_entry.user:
        if request.method == 'GET':
            updated_form.title.data = updated_entry.title
            updated_form.entry_date.data = updated_entry.entry_date
            updated_form.time_spent.data = updated_entry.time_spent
            updated_form.learned.data = updated_entry.learned
            updated_form.resources.data = updated_entry.resources
        elif updated_form.validate_on_submit():
            updated_entry.title = updated_form.title.data
            updated_entry.entry_date = updated_form.entry_date.data
            updated_entry.time_spent = updated_form.time_spent.data
            updated_entry.learned = updated_form.learned.data
            updated_entry.resources = updated_form.resources.data
            updated_entry.save()  
            flash('Entry updated!')
            return redirect(url_for('index', entry_id=entry_id))
    elif current_user != updated_entry.user:
        flash('Only the creator can edit this entry.', 'success')
        return render_template('index.html')        
    else:
        return render_template('edit.html', updated_entry=updated_entry, 
                                updated_form=updated_form)
    

@app.route('/entries/<int:entry_id>/delete', methods=('GET', 'POST'))
@login_required
def delete(entry_id):
    entry = models.Entry.get(models.Entry.id==entry_id)
    if current_user == entry.user:
        try:
            entry.delete_instance()
            flash('Entry deleted.', 'success')
            return redirect(url_for('index'))
        except models.IntegrityError:
            return render_template('404.html'), 404           
    else:
        flash('Entry can only be deleted by the creator', 'error')
        return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()  
    app.run(debug=True, port=8000, host='localhost')

