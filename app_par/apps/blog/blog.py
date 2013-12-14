import webapp2
import handler
import logging
import time
from google.appengine.api import memcache
from google.appengine.ext import db

class Post(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)

def newest_posts(update = False):
	key = "blog_entries"
	
	posts = memcache.get(key)
	if posts is None or update:
		logging.error("DB QUERY")
		posts = db.GqlQuery("SELECT * FROM Post "
						   "ORDER BY created DESC limit 10")
		posts = list(posts)
		memcache.set(key, posts)
		memcache.set("queried", time.time())
	return posts

def memcache_post(post_id, update = False):
	key = "post_" + post_id
	
	post = memcache.get(key)
	if post is None or update:
		post = Post.get_by_id(int(post_id))
		memcache.set(key, post)
		key_queried = "queried_post_" + post_id
		memcache.set(key_queried , time.time())
	return post

def time_since_queried(key_queried):
	time_queried = memcache.get(key_queried)
	time_passed = time.time() - time_queried
	return int(time_passed)
	

class BlogNewPost(handler.Handler):
	def get(self):
		self.render("blog_new.html")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")
	
		if subject and content:
			p = Post(subject = subject, content = content)
			p.put()
			newest_posts(True)
			x = str(p.key().id())
			self.redirect("/blog/%s" %x)
		else:
			error = "Sorry! You didn't provide a subject and a content!"
			self.render("blog_new.html", subject = subject, content = content, error = error)

class BlogHome(handler.Handler):
	def get(self):
		posts = newest_posts()
		modified = time_since_queried("queried")
		self.render("blog.html", posts = posts, modified = modified)
		
class PostHandler(handler.Handler):
	def get(self, post_id):
		blog_entry = memcache_post(post_id)
		modified = time_since_queried("queried_post_" + post_id)
		if blog_entry:
			self.render("blog_post.html", post = blog_entry, modified = modified)
		else:
			self.error(404)
