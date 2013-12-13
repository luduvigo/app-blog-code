import webapp2
import handler

class MainJSON(handler.BaseHandler):
	def get(self):
		self.response.write("Here JSON!")

class PermalinkJSON(handler.BaseHandler):
	def get(self):
		self.response.write("Permalink JSON")
