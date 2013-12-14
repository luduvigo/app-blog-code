import webapp2
import jinja2
import HTMLParser
import htmllib
import os
from string import letters
import signup
from apps.rot13 import rot13
from apps.blog import blog
import handler
import utility
import security
from apps.blog import json_output
from apps.blog import cache_utils

template_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Hello, Udacity!")	

class Welcome(handler.BaseHandler):
    def get(self):
        username = self.request.cookies.get('name')
        checked_username = security.check_secure_val(username)
        if utility.valid_username(checked_username):
            self.render('welcome.html', username = checked_username)
        else:
            self.redirect('/signup')

app = webapp2.WSGIApplication([('/', MainPage),
								('/rot13', rot13.Rot13), 
								('/blog/signup', signup.Signup),
								('/blog/welcome', Welcome),
								('/blog/login', signup.Login),
								('/blog/logout', signup.Logout),
								('/blog', blog.BlogHome),
								(r'/blog/(\d+)', blog.PostHandler),
								('/blog/newpost', blog.BlogNewPost),
								('/blog/.json', json_output.MainJSON),
								(r'/blog/(\d+).json', json_output.PermalinkJSON),
								('/blog/flush', cache_utils.FlushCache)],
								debug=True)		


