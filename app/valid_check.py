from flask import flash
from model import User


def registration_validation(userdata):
	user = User.query.filter_by(username=userdata['username']).first()
	email = User.query.filter_by(email=userdata['email']).first()
	if userdata['password'] != userdata['password_check']:
		flash("Passwords are not equal!", category="error")
		return True
	if user is not None:
		flash("Login already exist!", category="error")
		return True
	if email is not None:
		flash("Email already exist!", category="error")
		return True


def login_validation(userdata):
	user = User.query.filter_by(username=userdata['username']).first()
	if user is None:
		flash("Login does not exist", category="error")
		return True
	if not user.check_password(userdata['password']):
		flash("Wrong password", category="error")
		return True
