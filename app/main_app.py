from flask import Flask, render_template, url_for, request

app = Flask(__name__)


# flask -A .\app\main_app.py run


@app.route('/register', methods=["GET", "POST"])
def register():
	return render_template('registration.html', title='Страница регистрации пользователя')


@app.route('/login', methods=["GET", "POST"])
def login():
	return render_template('login.html', title='Вход в личный кабинет')


@app.route('/', methods=["GET", "POST"])
def main_page():
	return render_template('main_page.html', title='Главная страница')


@app.route('/task_page', methods=["GET", "POST"])
def task_page():
	return render_template('task_page.html', title='Профиль', username='Alexey')


@app.route('/logout', methods=["GET", "POST"])
def logout():
	print(request.form)
	return render_template('main_page.html', title='Главная страница')


@app.route('/addtask', methods=["GET", "POST"])
def add_task():
	if request.form['addTask']:
		print(request.form['task'])
	return render_template('task_page.html')


if __name__ == '__main__':
	app.run()
