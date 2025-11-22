from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from data import db_session
from data.users import User
from data.quests import Quest
from data.quest_reports import QuestReport
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Создаем папку для загрузок если её нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Маршрут для обслуживания файлов из корневой папки img/
@app.route('/img/<path:filename>')
def serve_img(filename):
    """Обслуживает файлы из корневой папки img/"""
    from flask import send_from_directory
    return send_from_directory('img', filename)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_form'

db_session.global_init('db/base.db')

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(User).get(user_id)
        return user
    finally:
        db_sess.close()

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    tg_name = StringField('TG', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired(), Length(min=3, message='Логин должен содержать минимум 3 символа')])
    email = EmailField('Email', validators=[DataRequired(), Email(message='Некорректный email')])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, message='Пароль должен содержать минимум 8 символов')])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')

class QuestReportForm(FlaskForm):
    quest_id = HiddenField('Quest ID')
    is_completed = SelectField('Проблема решена?', choices=[('', 'Выберите'), ('yes', 'Да'), ('no', 'Нет')], validators=[DataRequired()])
    photo = FileField('Прикрепите фотографии/видео', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'], 'Только изображения и видео!')])
    comment = TextAreaField('Добавьте описание (необязательно)')
    submit = SubmitField('Отправить')

def check_user_exists(login):
    """Проверяет, существует ли пользователь с данным логином"""
    db_sess = db_session.create_session()
    try:
        user = db_sess.query(User).filter(User.login == login).first()
        return user is not None
    finally:
        db_sess.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/authorization', methods=["GET", "POST"])
def login_form():
    if current_user.is_authenticated:
        # Если пользователь уже авторизован, редиректим на страницу, откуда пришли, или на s3.html
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect('/s3.html')
    
    form = LoginForm()
    
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            user = db_sess.query(User).filter(User.login == form.login.data).first()
            
            if not user:
                flash("Такого пользователя не существует", "error")
                return render_template('login.html', title='Авторизация', form=form)
            elif user.password != form.password.data:
                flash("Неверный пароль!!!", "error")
                return render_template('login.html', title='Авторизация', form=form)
            
            # Всегда авторизуемся без remember_me, чтобы сессия не сохранялась
            login_user(user, remember=False)
            
            # Редиректим на страницу, откуда пришли (next), или на s3.html по умолчанию
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('/s3.html')
        finally:
            db_sess.close()
    
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/registration', methods=["GET", "POST"])
def register_form():
    if current_user.is_authenticated:
        return redirect('/s3.html')
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        
        if check_user_exists(form.login.data):
            flash("Такой пользователь уже существует", "error")
            db_sess.close()
            return render_template('registration.html', title='Регистрация', form=form)
        
        user = User()
        user.login = form.login.data
        user.email = form.email.data
        user.tg_name = form.tg_name.data
        user.password = form.password.data
        
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()

        flash("Регистрация успешна! Войдите в систему.", "success")
        return redirect(url_for('login_form'))
    
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/s2index')
@login_required
def s2index():
    return render_template('s2index.html')

@app.route('/s3.html')
def s3():
    return render_template('s3.html')

@app.route('/app')
@app.route('/dashboard')
@login_required
def dashboard():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    db_sess.close()
    return render_template('dashboard.html', user=user)

@app.route('/quests')
@login_required
def quests_list():
    """Список всех квестов"""
    db_sess = db_session.create_session()
    all_quests = db_sess.query(Quest).all()
    
    # Проверяем, какие квесты уже взяты пользователем
    user_reports = db_sess.query(QuestReport).filter(QuestReport.user_id == current_user.id).all()
    taken_quest_ids = {report.quest_id for report in user_reports}
    
    db_sess.close()
    return render_template('quests_list.html', quests=all_quests, taken_quest_ids=taken_quest_ids)

@app.route('/quest/<int:quest_id>')
@login_required
def quest_detail(quest_id):
    """Детальная страница квеста"""
    db_sess = db_session.create_session()
    quest = db_sess.query(Quest).get(quest_id)
    
    if not quest:
        flash("Квест не найден", "error")
        db_sess.close()
        return redirect(url_for('quests_list'))
    
    # Проверяем, есть ли уже отчет от этого пользователя
    existing_report = db_sess.query(QuestReport).filter(
        QuestReport.quest_id == quest_id,
        QuestReport.user_id == current_user.id
    ).first()
    
    is_taken = existing_report is not None
    # Форма показывается только если квест принят
    form = QuestReportForm() if is_taken else None
    
    db_sess.close()
    return render_template('quest_detail.html', quest=quest, is_taken=is_taken, form=form, report=existing_report, show_form=False)

@app.route('/quest/<int:quest_id>/take', methods=['POST'])
@login_required
def take_quest(quest_id):
    """Принять квест"""
    db_sess = db_session.create_session()
    quest = db_sess.query(Quest).get(quest_id)
    
    if not quest:
        flash("Квест не найден", "error")
        db_sess.close()
        return redirect(url_for('quests_list'))
    
    # Проверяем, не взят ли уже квест
    existing_report = db_sess.query(QuestReport).filter(
        QuestReport.quest_id == quest_id,
        QuestReport.user_id == current_user.id
    ).first()
    
    if existing_report:
        flash("Вы уже взяли этот квест", "error")
        db_sess.close()
        return redirect(url_for('quest_detail', quest_id=quest_id))
    
    # Создаем отчет (квест взят, но еще не выполнен)
    report = QuestReport()
    report.quest_id = quest_id
    report.user_id = current_user.id
    report.is_completed = False
    report.comment = ""  # Пустой комментарий, чтобы отличать от отправленного отчета
    
    # Обновляем статус квеста
    quest.status = 'в исполнении'
    
    db_sess.add(report)
    db_sess.commit()
    db_sess.close()
    
    flash("Квест принят! Теперь вы можете оставить отчет.", "success")
    return redirect(url_for('quest_detail', quest_id=quest_id))

@app.route('/quest/<int:quest_id>/report', methods=['POST'])
@login_required
def submit_quest_report(quest_id):
    """Отправить отчет по квесту"""
    db_sess = db_session.create_session()
    quest = db_sess.query(Quest).get(quest_id)
    
    if not quest:
        flash("Квест не найден", "error")
        db_sess.close()
        return redirect(url_for('quests_list'))
    
    # Находим существующий отчет
    report = db_sess.query(QuestReport).filter(
        QuestReport.quest_id == quest_id,
        QuestReport.user_id == current_user.id
    ).first()
    
    if not report:
        flash("Сначала примите квест", "error")
        db_sess.close()
        return redirect(url_for('quest_detail', quest_id=quest_id))
    
    form = QuestReportForm()
    
    if form.validate_on_submit():
        report.is_completed = (form.is_completed.data == 'yes')
        report.comment = form.comment.data if form.comment.data else ''
        
        # Обработка загруженного фото
        if form.photo.data:
            filename = secure_filename(f"{quest_id}_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{form.photo.data.filename.rsplit('.', 1)[1].lower()}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.photo.data.save(filepath)
            report.photo_path = f"static/uploads/{filename}"
        
        # Обновляем статус квеста в зависимости от результата
        if report.is_completed:
            user = db_sess.query(User).get(current_user.id)
            if user:
                user.balance += quest.points
            quest.status = 'выполнена'
            flash(f"Квест выполнен! Вам начислено {quest.points} коинов.", "success")
        else:
            # Если квест не выполнен, оставляем статус "в исполнении"
            quest.status = 'в исполнении'
            flash("Отчет отправлен. Квест не выполнен.", "info")
        
        # Сохраняем изменения (объекты уже в сессии, просто коммитим)
        try:
            db_sess.commit()
        except Exception as e:
            db_sess.rollback()
            flash("Ошибка при сохранении отчета", "error")
            db_sess.close()
            return redirect(url_for('quest_detail', quest_id=quest_id))
        
        db_sess.close()
        return redirect(url_for('quest_detail', quest_id=quest_id))
    
    db_sess.close()
    flash("Ошибка при отправке отчета", "error")
    return redirect(url_for('quest_detail', quest_id=quest_id))

if __name__ == '__main__':
    app.debug = True
    app.run(port=8002, host='127.0.0.1')