from flask import Flask, render_template, url_for, request, redirect, session, g
from configuration import Configuration
from valid_check import registration_validation, login_validation
from model import User, AddTask, db
from functools import wraps
from weather import weather

app = Flask(__name__)
app.config.from_object(Configuration)

db.init_app(app)


def login_required(function):
	@wraps(function)
	def decorated_function(*args, **kwargs):
		if 'username' not in session:
			return redirect(url_for('main_page'))
		return function(*args, **kwargs)

	return decorated_function


def login_not_required(function):
	@wraps(function)
	def decorated_function(*args, **kwargs):
		if 'username' in session:
			return redirect(url_for('task_page'))
		return function(*args, **kwargs)

	return decorated_function


@app.route('/register', methods=["GET", "POST"])
@login_not_required
def register():
	if request.method == "POST":
		if registration_validation(request.form):
			return render_template('registration.html', title='Страница регистрации пользователя')

		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		user = User(username=username, email=email)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()
		session['username'] = username
		return redirect(url_for('task_page'))

	return render_template('registration.html', title='Страница регистрации пользователя')


@app.route('/login', methods=["GET", "POST"])
@login_not_required
def login():
	if request.method == "POST":
		username = request.form['username']
		if login_validation(request.form):
			return render_template('login.html', title='Вход в личный кабинет')
		session['username'] = username
		return redirect(url_for('task_page'))
	return render_template('login.html', title='Вход в личный кабинет')


@app.route('/', methods=["GET", "POST"])
def main_page():
	return render_template('main_page.html', title='Главная страница')


@app.route('/task_page', methods=["GET", "POST"])
@login_required
def task_page():
	local_weather = weather()
	username = session.get('username')
	user_id = User.query.filter_by(username=username).first()
	all_user_tasks = AddTask.query.filter_by(user_id=user_id.id).all()
	return render_template('task_page.html', title='Профиль', username=username, tasks=all_user_tasks,
						   city=local_weather.json['location']['name'], temp=local_weather.json['current']['temp_c'])


@app.route('/logout', methods=["GET", "POST"])
def logout():
	session.pop('username')
	return render_template('main_page.html', title='Главная страница')


@app.route('/addtask', methods=["GET", "POST"])
def add_task():
	username = session.get('username')
	if request.form['task']:
		user_id = User.query.filter_by(username=username).first()
		task = AddTask(body=request.form['task'], user_id=user_id.id)
		db.session.add(task)
		db.session.commit()
		return redirect(url_for('task_page'))


@app.route('/task/<id>/<user_id>/delete', methods=["GET", "POST"])
def delete(id, user_id):
	if request.method == "POST":
		task = AddTask.query.filter_by(id=int(id), user_id=int(user_id)).first()
		if task is not None:
			db.session.delete(task)
			db.session.commit()
			return redirect(url_for('task_page'))


@app.route('/task/<id>/<user_id>/done', methods=["GET", "POST"])
def done(id, user_id):
	if request.method == "POST":
		task = AddTask.query.filter_by(id=int(id), user_id=int(user_id)).first()
		if task is not None:
			if task.task_ready_status:
				task.task_ready_status = 0
				db.session.commit()
			else:
				task.task_ready_status = 1
				db.session.commit()
			return redirect(url_for('task_page'))


if __name__ == '__main__':
	app.run()
	with app.app_context():
		db.create_all()
