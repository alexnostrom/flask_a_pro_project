from flask import flash
from model import User


def registration_validation(userdata):
	user = User.query.filter_by(username=userdata['username']).first()
	email = User.query.filter_by(email=userdata['email']).first()
	if userdata['password'] != userdata['password_check']:
		flash("Пароли не совпадают!", category="error")
		return True
	if user is not None:
		flash("Логин уже существует!", category="error")
		return True
	if email is not None:
		flash("Email уже существует!", category="error")
		return True


def login_validation(userdata):
	user = User.query.filter_by(username=userdata['username']).first()
	if user is None:
		flash("Указанный логин не существует", category="error")
		return True
	if not user.check_password(userdata['password']):
		flash("Неверный пароль", category="error")
		return True