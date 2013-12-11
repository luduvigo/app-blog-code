import webapp2
import jinja2
import cgi
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

template_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

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
								('/signup', signup.Signup),
								('/welcome', Welcome),
								('/blog', blog.BlogHome),
								(r'/blog/(\d+)', blog.PostHandler),
								('/blog/newpost', blog.BlogNewPost)],
								debug=True)		


