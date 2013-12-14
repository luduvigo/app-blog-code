import webapp2
import handler
from google.appengine.api import memcache

class FlushCache(handler.BaseHandler):
	def get(self):
		memcache.flush_all()
		self.redirect('/blog')
		
