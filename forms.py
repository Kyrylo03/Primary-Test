from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Імʼя користувача', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Увійти')

class RegisterForm(FlaskForm):
    username = StringField('Імʼя користувача', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Підтвердьте пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')

class TestForm(FlaskForm):
    q1 = IntegerField('1. 2 + 3 =', validators=[DataRequired()])
    q2 = IntegerField('2. 7 - 4 =', validators=[DataRequired()])
    q3 = IntegerField('3. 5 * 2 =', validators=[DataRequired()])
    q4 = IntegerField('4. 9 // 3 =', validators=[DataRequired()])
    q5 = IntegerField('5. 6 + 7 =', validators=[DataRequired()])
    q6 = IntegerField('6. 12 - 5 =', validators=[DataRequired()])
    q7 = IntegerField('7. 3 * 3 =', validators=[DataRequired()])
    q8 = IntegerField('8. 8 // 2 =', validators=[DataRequired()])
    q9 = IntegerField('9. 10 + 5 =', validators=[DataRequired()])
    q10 = IntegerField('10. 4 * 2 =', validators=[DataRequired()])
    submit = SubmitField('Завершити')

    def evaluate(self):
        answers = {
            'q1': 5, 'q2': 3, 'q3': 10, 'q4': 3, 'q5': 13,
            'q6': 7, 'q7': 9, 'q8': 4, 'q9': 15, 'q10': 8
        }
        score = 0
        for field, correct in answers.items():
            if getattr(self, field).data == correct:
                score += 1
        return score