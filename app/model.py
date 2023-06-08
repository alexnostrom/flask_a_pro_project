from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), nullable=False, unique=True)
	email = db.Column(db.String(120), nullable=False, unique=True)
	password_hash = db.Column(db.String(120))
	tasks = db.relationship('AddTask', lazy=True)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class AddTask(db.Model):
	__tablename__ = 'tasks'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text(140))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
