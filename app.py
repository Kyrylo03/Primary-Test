from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from models import db, User, TestResult
from forms import LoginForm, RegisterForm, TestForm
from extensions import login_manager
from config import Config
from admin import init_admin

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

# Ініціалізація бази та адмінки
with app.app_context():
    db.create_all()
    init_admin(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Неправильне імʼя користувача або пароль')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])  # Додано підтримку POST
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Реєстрація успішна. Увійдіть.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    form = TestForm()
    if form.validate_on_submit():
        correct_answers = form.evaluate()
        grade = calculate_grade(correct_answers)
        grade_numeric = float(correct_answers)

        result = TestResult(
            user_id=current_user.id,
            score=correct_answers,
            grade=grade,
            grade_numeric=grade_numeric
        )
        db.session.add(result)
        db.session.commit()
        return redirect(url_for('result'))
    return render_template('test.html', form=form)

@app.route('/result')
@login_required
def result():
    results = TestResult.query.filter_by(user_id=current_user.id).all()
    avg_score = sum(r.score for r in results) / len(results)
    avg_grade = calculate_grade(avg_score)
    return render_template('result.html', score=avg_score, grade=avg_grade)

def calculate_grade(score):
    if score >= 9:
        return 'A'
    elif score >= 8:
        return 'B'
    elif score >= 6:
        return 'C'
    elif score >= 5:
        return 'D'
    else:
        return 'F'

if __name__ == 'main':
    app.run(debug=True)