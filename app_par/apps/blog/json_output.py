import webapp2
import handler
import json
import blog
from google.appengine.ext import db

class MainJSON(handler.BaseHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
		posts = db.GqlQuery("SELECT * FROM Post "
							"ORDER BY created DESC limit 10")
		time_fmt = '%c'
		list1 = []
		for p in posts:

			list1.append("{'subject' : '" + blog_entry.subject +"',"
						" 'content' : '" + blog_entry.content + "',"
						" 'created' : '" + blog_entry.created.strftime(time_fmt) + "',"
						" 'last_modified' : '" + blog_entry.last_modified.strftime(time_fmt) + "'}")

		json1 = json.dumps(list1)
		self.response.write(json1)

class PermalinkJSON(handler.BaseHandler):
	def get(self, post_id):
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
		time_fmt = '%c'
		blog_entry = blog.Post.get_by_id(int(post_id))
		if blog_entry:
			json1 = json.dumps("{'subject' : '" + blog_entry.subject +"',"
								" 'content' : '" + blog_entry.content + "',"
								" 'created' : '" + blog_entry.created.strftime(time_fmt) + "',"
								" 'last_modified' : '" + blog_entry.last_modified.strftime(time_fmt) + "'}")
			self.response.write(json1)
		else:
			self.error(404)
