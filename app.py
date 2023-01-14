from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    age = db.Column(db.Text)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Text, primary_key=True)
    text = db.Column(db.Text)
    image = db.Column(db.Text)
    right_answer = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    id_question = db.Column(db.Text, db.ForeignKey('questions.id'), primary_key=True)
    answer = db.Column(db.Text)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/questionnaire")
def agree():
    return render_template('questionnaire.html')

@app.route("/form")
def form():
    questions = Questions.query.all()
    return render_template(
        'form.html',
        questions=questions)

@app.route("/stat")
def stat():
    total = {}
    age = {}
    gender = {}
    education = {}
    questions = {}
    
    total['total_count'] = User.query.count()
    
    age['До 20 лет'] = db.session.query(
        func.count(User.age)
    ).where(User.age == 'До 20 лет').one()[0]
    age['20-35'] = db.session.query(
        func.count(User.age)
    ).where(User.age == '20-35').one()[0]
    age['35-50'] = db.session.query(
        func.count(User.age)
    ).where(User.age == '35-50').one()[0]
    age['50+'] = db.session.query(
        func.count(User.age)
    ).where(User.age == '50+').one()[0]
    
    gender['Другой'] = db.session.query(
        func.count(User.gender)
    ).where(User.gender == 'Другой').one()[0]
    gender['М'] = db.session.query(
        func.count(User.gender)
    ).where(User.gender == 'М').one()[0]
    gender['Ж'] = db.session.query(
        func.count(User.gender)
    ).where(User.gender == 'Ж').one()[0]
    
    education['Среднее'] = db.session.query(
        func.count(User.education)
    ).where(User.education == 'Среднее').one()[0]
    education['Неоконченное высшее'] = db.session.query(
        func.count(User.education)
    ).where(User.education == 'Неоконченное высшее').one()[0]
    education['Высшее (бакалавриат, специалитет)'] = db.session.query(
        func.count(User.education)
    ).where(User.education == 'Высшее (бакалавриат, специалитет)').one()[0]
    education['Магистратура'] = db.session.query(
        func.count(User.education)
    ).where(User.education == 'Магистратура').one()[0]
    education['Научная степень (кандидат наук, доктор наук, PhD)'] = db.session.query(
        func.count(User.education)
    ).where(User.education == 'Научная степень (кандидат наук, доктор наук, PhD)').one()[0]
    
    questions['Никола Тесла'] = [db.session.query(Questions.right_answer).where(Questions.text == 'Никола Тесла').one()[0],
                                 round(db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Никола Тесла', Answers.answer == Questions.right_answer).one()[0] / db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Никола Тесла').one()[0] * 100),
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Никола Тесла', Answers.answer == 'Математик').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Никола Тесла', Answers.answer == 'Лингвист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Никола Тесла', Answers.answer == 'Экономист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Никола Тесла', Answers.answer == 'Физик').one()[0]]
    questions['Фердинанд де Соссюр'] = [db.session.query(Questions.right_answer).where(Questions.text == 'Фердинанд де Соссюр').one()[0],
                                 round(db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Фердинанд де Соссюр', Answers.answer == Questions.right_answer).one()[0] / db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Фердинанд де Соссюр').one()[0] * 100),
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Фердинанд де Соссюр', Answers.answer == 'Математик').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Фердинанд де Соссюр', Answers.answer == 'Лингвист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Фердинанд де Соссюр', Answers.answer == 'Экономист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Фердинанд де Соссюр', Answers.answer == 'Физик').one()[0]]
    questions['Исаак Ньютон'] = [db.session.query(Questions.right_answer).where(Questions.text == 'Исаак Ньютон').one()[0],
                                 round(db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Исаак Ньютон', Answers.answer == Questions.right_answer).one()[0] / db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Исаак Ньютон').one()[0] * 100),
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Исаак Ньютон', Answers.answer == 'Математик').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Исаак Ньютон', Answers.answer == 'Лингвист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Исаак Ньютон', Answers.answer == 'Экономист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Исаак Ньютон', Answers.answer == 'Физик').one()[0]]
    questions['Игорь Александрович Мельчук'] = [db.session.query(Questions.right_answer).where(Questions.text == 'Игорь Александрович Мельчук').one()[0],
                                 round(db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Игорь Александрович Мельчук', Answers.answer == Questions.right_answer).one()[0] / db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Игорь Александрович Мельчук').one()[0] * 100),
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Игорь Александрович Мельчук', Answers.answer == 'Математик').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Игорь Александрович Мельчук', Answers.answer == 'Лингвист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Игорь Александрович Мельчук', Answers.answer == 'Экономист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Игорь Александрович Мельчук', Answers.answer == 'Физик').one()[0]]
    questions['Адам Смит'] = [db.session.query(Questions.right_answer).where(Questions.text == 'Адам Смит').one()[0],
                                 round(db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Адам Смит', Answers.answer == Questions.right_answer).one()[0] / db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Адам Смит').one()[0] * 100),
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Адам Смит', Answers.answer == 'Математик').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Адам Смит', Answers.answer == 'Лингвист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Адам Смит', Answers.answer == 'Экономист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Адам Смит', Answers.answer == 'Физик').one()[0]]
    questions['Блез Паскаль'] = [db.session.query(Questions.right_answer).where(Questions.text == 'Блез Паскаль').one()[0],
                                 round(db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Блез Паскаль', Answers.answer == Questions.right_answer).one()[0] / db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Блез Паскаль').one()[0] * 100),
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Блез Паскаль', Answers.answer == 'Математик').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Блез Паскаль', Answers.answer == 'Лингвист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Блез Паскаль', Answers.answer == 'Экономист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Блез Паскаль', Answers.answer == 'Физик').one()[0]]
    questions['Пифагор'] = [db.session.query(Questions.right_answer).where(Questions.text == 'Пифагор').one()[0],
                                 round(db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Пифагор', Answers.answer == Questions.right_answer).one()[0] / db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Пифагор').one()[0] * 100),
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Пифагор', Answers.answer == 'Математик').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Пифагор', Answers.answer == 'Лингвист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Пифагор', Answers.answer == 'Экономист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Пифагор', Answers.answer == 'Физик').one()[0]]
    questions['Карл Маркс'] = [db.session.query(Questions.right_answer).where(Questions.text == 'Карл Маркс').one()[0],
                                 round(db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Карл Маркс', Answers.answer == Questions.right_answer).one()[0] / db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Карл Маркс').one()[0] * 100),
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Карл Маркс', Answers.answer == 'Математик').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Карл Маркс', Answers.answer == 'Лингвист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Карл Маркс', Answers.answer == 'Экономист').one()[0],
                                 db.session.query(func.count(Answers.answer)).join(Questions).where(Questions.text == 'Карл Маркс', Answers.answer == 'Физик').one()[0]]
    
    return render_template('stat.html', total=total, age=age, gender=gender, education=education, questions=questions)

@app.route("/process", methods=['get'])
def process():
    if not request.args:
        return redirect(url_for('form'))
    gender = request.args.get('gender')
    education = request.args.get('education')
    age = request.args.get('age')
    user = User(
        gender=gender,
        education=education,
        age=age
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    for q in Questions.query.all():
        answer = Answers(id_user=user.id, id_question=q.id, answer=request.args.get(q.id))
        db.session.add(answer)
        db.session.commit()
    return redirect(url_for('stat'))

if __name__ == '__main__':
    app.run(debug=False)