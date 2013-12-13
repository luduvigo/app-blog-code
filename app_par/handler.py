import webapp2
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class BaseHandler(webapp2.RequestHandler):
	def render(self, template, **kw):
		self.response.out.write(self.render_str(template, **kw))

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
