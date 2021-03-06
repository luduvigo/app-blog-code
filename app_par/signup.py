import webapp2
import re
import handler
import utility
import security
import logging
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
		if (username_received != "luduvigo"):
			self.redirect('/')
			return
		password_received = self.request.get('password') 
		confirmation_received = self.request.get('verify')
		email_received = self.request.get('email')

		check_user = db.GqlQuery("SELECT * FROM User WHERE username = "
								"'" + username_received + "'").get()

		params = dict(username = username_received, email = email_received)

		has_error = False
		if check_user:
			params['error_username'] = "The username already exists." 
			has_error = True
		else:
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

class Login(handler.BaseHandler):
	def get(self):
		self.render('login.html')

	def post(self):
		username_rec = self.request.get('username')
		password_rec = self.request.get('password')

		has_error = False
		params = dict()
		user = db.GqlQuery("SELECT * FROM User WHERE username = '" + username_rec + "'").get()
		if user == None:
			params['error_login'] = "Invalid input"
			has_error = True
		else:    
			password_encoded = security.valid_pw(username_rec, password_rec, user.password)
			if(password_encoded == True):
				self.response.headers['Content-Type'] = 'text/plain'
				cookie_value = security.make_secure_val(str(username_rec))
				self.response.headers.add_header('Set-Cookie', 'name=' + cookie_value + '; Path=/')
				self.redirect('/welcome')
			else:
				params['error_login'] = "Invalid input"
				has_error = True
		if has_error:
			self.render('login.html', **params)

class Logout(handler.BaseHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.headers.add_header('Set-Cookie', 'name=''; Path=/')
		self.redirect('/blog/signup')
