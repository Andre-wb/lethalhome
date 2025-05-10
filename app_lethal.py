from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from datetime import datetime
import re
from dotenv import load_dotenv
import os
load_dotenv()



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SQLALCHEMY_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///host_database_lethal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Пароли должны совпадать!')])
    confirm = PasswordField('Repeat Password')


class InputForm(Form):
    input = StringField('Input', [validators.DataRequired()])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def main():
    comments = Comment.query.all()
    return render_template('main_page.html', comments=comments)

@app.route('/main')
def index():
    comments = Comment.query.all()
    return render_template('main_page.html', comments=comments)


@app.route('/main/store')
def output_store():
    comments = Comment.query.all()
    return render_template('store_page.html', comments=comments)


@app.route('/main/scrap')
def output_scrap():
    comments = Comment.query.all()
    return render_template('scrap_page.html', comments=comments)


@app.route('/main/terminal')
def output_terminal():
    comments = Comment.query.all()
    return render_template('terminal_page.html', comments=comments)


@app.route('/main/mobs')
def output_mobs():
    comments = Comment.query.all()
    return render_template('mobs_page.html', comments=comments)


@app.route('/main/planets')
def output_planets():
    comments = Comment.query.all()
    return render_template('planet_page.html', comments=comments)


@app.route('/main/complex')
def complex():
    comments = Comment.query.all()
    return render_template('complex_page.html', comments=comments)


@app.route('/main/weather')
def output_weather():
    comments = Comment.query.all()
    return render_template('weather_page.html', comments=comments)


@app.route('/')
def output_base():
    comments = Comment.query.all()
    return render_template('main.html', comments=comments)


@app.route('/error')
def error():
    return render_template('error_page.html')


@app.route('/log_index', methods=['GET', 'POST'])
def log_index():
    if request.method == 'POST':
        user_input = request.form.get('input', '').strip().lower()
        if user_input == 'вход':
            return redirect(url_for('login'))
        elif user_input == 'регистрация':
            return redirect(url_for('register'))
        else:
            flash('Неправильная команда! Введите "вход" или "регистрация".')
            return redirect(url_for('log_index'))
    return render_template('log_index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if not username and not email and not password:
            flash('Пожалуйста, введите данные от аккаунта.')
            return redirect(url_for('register'))
        if not re.search(r'\d', password) or not re.search(r'[a-zA-Z]', password) or len(password) < 8:
            flash('Пароль должен состоять из букв и цифр, и быть длиной не менее 8 символов', 'error')
            return redirect(url_for('register'))
        else:
            if confirm != password:
                flash('Пароли должны совпадать.')
            if not username:
                flash('Пожалуйста, введите имя пользователя.')
                return redirect(url_for('register'))
            if not email:
                flash('Пожалуйста, введите эл.почту.')
                return redirect(url_for('register'))
            if not password or not confirm:
                flash('Пожалуйста, введите пароль.')
                return redirect(url_for('register'))
        if existing_user:
            flash('Данное имя занято, выберите другое.')
            return redirect(url_for('register'))
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            try:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            except:
                db.session.rollback()
    return render_template('register_page.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not username and not password:
            flash('Пожалуйста, введите данные от аккаунта.')
            return redirect(url_for('login'))
        else:
            if not username:
                flash('Пожалуйста, введите имя пользователя.')
                return redirect(url_for('login'))
            if not password:
                flash('Пожалуйста, введите пароль.')
                return redirect(url_for('login'))
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Неправильные данные от аккаунта.')
        pass
    return render_template('login_page.html')


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


class DeleteAccountForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Delete Account')


@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        if current_user.is_authenticated:
            username = request.form.get('username')
            password = request.form.get('password')
            try:
                db.session.delete(current_user)
                db.session.commit()
                return redirect(url_for('index'))
            except:
                try:
                    db.session.rollback()
                except:
                    return render_template('error_page.html')
    return render_template('delete_account_page.html')


@app.route('/add_comment', methods=['POST'])
@login_required
def add_comment():
    text = request.form['text']
    comment = Comment(text=text, user_id=current_user.id, date=datetime.utcnow())
    try:
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        try:
            db.session.rollback()
        except:
            return render_template('error_page.html')


@app.route('/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        flash('Вы не авторизованы как автор этого комментария.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        comment.text = request.form['text']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            try:
                db.session.rollback()
            except:
                return render_template('error_page.html')
    return render_template('edit_comment_page.html', comment=comment)


@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        flash('Вы не авторизованы как автор этого комментария.')
        return redirect(url_for('index'))
    try:
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        try:
            db.session.rollback()
        except:
            return render_template('error_page.html')

if __name__ == '__main__':
    app.run(debug=True)
