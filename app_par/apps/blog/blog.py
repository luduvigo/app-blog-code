import webapp2
import handler

from google.appengine.ext import db

class Post(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)

class BlogNewPost(handler.Handler):
	def get(self):
		self.render("blog_new.html")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")
	
		if subject and content:
			p = Post(subject = subject, content = content)
			p.put()
			x = str(p.key().id())
			self.redirect("/blog/%s" %x)
		else:
			error = "Sorry! You didn't provide a subject and a content!"
			self.render("blog_new.html", subject = subject, content = content, error = error)

class BlogHome(handler.Handler):
	def get(self):
		posts = db.GqlQuery("SELECT * FROM Post "
						   "ORDER BY created DESC limit 10")
		self.render("blog.html", posts = posts)
		
class PostHandler(handler.Handler):
	def get(self, post_id):
		blog_entry = Post.get_by_id(int(post_id))
		if blog_entry:
			self.render("blog_post.html", post = blog_entry)
		else:
			self.error(404)
