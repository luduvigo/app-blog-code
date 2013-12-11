import webapp2
import re
import handler
import utility
import security
from google.appengine.ext import db

class User(db.Model):
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.StringProperty(required = False)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)


class Signup(handler.BaseHandler):
	def get(self):
		self.render('signup.html')
	def post(self):
		
		username_received = self.request.get('username')
		password_received = self.request.get('password') 
		confirmation_received = self.request.get('verify')
		email_received = self.request.get('email')

		params = dict(username = username_received, email = email_received)

		has_error = False
	
		if not utility.valid_username(username_received):
			params['error_username'] = "That's not a valid username." 
			has_error = True

		if not utility.valid_password(password_received):
			params['error_password'] = "That's not a valid password." 
			has_error = True
		elif password_received != confirmation_received:
			params['error_verify'] = "Your passwords didn't match."
			has_error = True

		if not utility.valid_email(email_received):
			params['error_email'] = "That's not a valid email." 
			has_error = True
		
		if has_error:
			self.render('signup.html', **params)

		else:
			password = security.make_pw_hash(username_received, password_received)
			u = User(username = username_received, password = password, email = email_received)
			u.put()
			self.response.headers['Content-Type'] = 'text/plain'
			cookie_value = security.make_secure_val(str(username_received))
			self.response.headers.add_header('Set-Cookie', 'name=' + cookie_value + '; Path=/')
			self.redirect('/welcome')
