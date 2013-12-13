import webapp2
import handler
import json
from google.appengine.ext import db

class MainJSON(handler.BaseHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
		posts = db.GqlQuery("SELECT * FROM Post "
							"ORDER BY created DESC limit 10")
		list1 = []
		for p in posts:
			list1.append("{'subject' : '" + p.subject +"', 'content' : '" + p.content+"' }")

		json1 = json.dumps(list1)
		self.response.write(json1)

class PermalinkJSON(handler.BaseHandler):
	def get(self, post_id):
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'

		posts = db.GqlQuery("SELECT * FROM Post "
							"WHERE id = '")
		blog_entry = Post.get_by_id(int(post_id))
		if blog_entry:
			json1 = json.dumps("{'subject' : '" + blog_entry.subject +"', 'content' : '" + bòpo.content+"' }")
		else:
			self.error(404)
