import webapp2
import re
import handler
import utility


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
			self.redirect('/welcome?username=' + username_received)
