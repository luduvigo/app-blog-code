import webapp2
import jinja2
import cgi
import re
import HTMLParser
import htmllib
import os
from string import letters
from apps.rot13 import rot13
from apps.blog import blog

template_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def escape_html(s):
    return cgi.escape(s, quote = True)

def html_decode(s):
	html_parser = HTMLParser.HTMLParser()
	return html_parser.unescape(s)

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    # this has to be last:
    s = s.replace("&amp;", "&")
    return s

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
	return not email or EMAIL_RE.match(email)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Hello, Udacity!")	

class BaseHandler(webapp2.RequestHandler):
	def render(self, template, **kw):
		self.response.out.write(render_str(template, **kw))

class Signup(BaseHandler):
	def get(self):
		self.render('signup.html')
	def post(self):
		
		username_received = self.request.get('username')
		password_received = self.request.get('password') 
		confirmation_received = self.request.get('verify')
		email_received = self.request.get('email')

		params = dict(username = username_received, email = email_received)

		has_error = False
	
		if not valid_username(username_received):
			params['error_username'] = "That's not a valid username." 
			has_error = True

		if not valid_password(password_received):
			params['error_password'] = "That's not a valid password." 
			has_error = True
		elif password_received != confirmation_received:
			params['error_verify'] = "Your passwords didn't match."
			has_error = True

		if not valid_email(email_received):
			params['error_email'] = "That's not a valid email." 
			has_error = True
		
		if has_error:
			self.render('signup.html', **params)

		else:
			self.redirect('/welcome?username=' + username_received)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/signup')

app = webapp2.WSGIApplication([('/', MainPage),
								('/rot13', rot13.Rot13), 
								('/signup', Signup),
								('/welcome', Welcome),
								('/blog', blog.BlogHome),
								(r'/blog/(\d+)', blog.PostHandler),
								('/blog/newpost', blog.BlogNewPost)],
								debug=True)		


