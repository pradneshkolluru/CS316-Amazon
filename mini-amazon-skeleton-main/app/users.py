from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data):
            flash('Congratulations, you are now a registered user! Log into your account above.')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/account', methods = ['POST', 'GET'])
def show_info():
    return render_template('account.html')
    
@bp.route('/updateEmail', methods = ['POST', 'GET'])
def update_email():
    if current_user.is_authenticated:
        newEmail = request.form.get("newEmail")
        if User.email_exists(newEmail):
            flash('Already a user with this email.')
        else:
            User.update_email(id=current_user.id, newInput=newEmail)
        return redirect(url_for('users.show_info'))
@bp.route('/updateFirstName', methods = ['POST', 'GET'])
def update_first_name():
    if current_user.is_authenticated:
        newFirst = request.form.get("newFirst")
        User.update_firstName(id=current_user.id, newInput=newFirst)
        return redirect(url_for('users.show_info'))
@bp.route('/updateLastName', methods = ['POST', 'GET'])
def update_last_name():
    if current_user.is_authenticated:
        newFirst = request.form.get("newLast")
        User.update_lastName(id=current_user.id, newInput=newFirst)
        return redirect(url_for('users.show_info'))
@bp.route('/updateAddress', methods = ['POST', 'GET'])
def update_address():
    if current_user.is_authenticated:
        newAddress = request.form.get("newAddress")
        User.update_address(id=current_user.id, newInput=newAddress)
        return redirect(url_for('users.show_info'))

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
