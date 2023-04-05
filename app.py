# установите необходимые пакеты
# pip install flask Flask-SQLAlchemy watchdog

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # начало работы с Flask-SQLAlchemy https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False  # о конфигурации https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
db = SQLAlchemy(app)


class Todo(db.Model):  # подробнее о db.Model https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')  
def index():
    todo_list = Todo.query.all()  # метод запроса данных https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
    return render_template('index.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])  # HTTP-методы https://www.techwithtim.net/tutorials/flask/http-methods-get-post/
def add():
    title = request.form["title"]
    new_todo = Todo(title=title,complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))
    
if __name__ == "__main__":
    with app.app_context():  # закрывает соединение с БД после завершение работы
        db.create_all()  # запуск базы данных https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#create-the-tables
        # new_todo = Todo(title="Приветствие")  # пробуем создать заметку
        # db.session.add(new_todo)
        # db.session.commit()
    app.run(debug=True)
