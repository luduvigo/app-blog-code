import webapp2
import re
import handler
import utility


################################
# Utilities

SECRET = 'imsosecretppzz'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    punto = h.find(",")
    salt = h[punto + 1:]
    if h == make_pw_hash(name, pw, salt):
        return True

################################


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
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.headers.add_header('Set-Cookie', 'name= %s' % username_received)
			self.redirect('/welcome')
