import webapp2
import handler
import logging
from google.appengine.api import memcache
from google.appengine.ext import db

class Wiki(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)


class EditPage(handler.Handler):
	def get(self, page_name):
		self.render("wiki_edit.html", page_name = page_name[1:])

	def post(self, page_name):
		title = page_name[1:]
		content = self.request.get("content")
	
		if title and content:
			p = Wiki(title = title, content = content)
			p.put()
			self.redirect("/wiki%s" %page_name)
		else:
			error = "Sorry! You didn't provide a title and a content!"
			self.render("wiki_edit.html", page_name = page_name, content = content, error = error)
		
class WikiPage(handler.Handler):
	def get(self, page_name):
		logging.error("DB QUERY")
		logging.error(page_name)
		wiki = db.GqlQuery("SELECT * FROM Wiki "
						   "WHERE title = '%s'" %page_name[1:]).get()
		if wiki is None:
			self.redirect("/wiki/_edit%s" %page_name)
		else:	
			self.render("wiki_entry.html", wiki = wiki)
