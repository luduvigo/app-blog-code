import os
import webapp2
import jinja2
import urllib2
from xml.dom import minidom

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
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

IP_URL = "http://api.hostip.info/?ip="
def getCoords(ip):
	url = IP_URL + ip
	content = None
	try:
		content = urllib2.urlopen(url).read()
	except urllib2.URLError:
		return

	if content:
		dom = minidom.parseString(content)
		coords = dom.getElementsByTagName('gml:coordinates')
		if coords and coords[0].childNodes[0].nodeValue:
			lon, lat = coords[0].childNodes[0].nodeValue.split(',')
			return db.GeoPt(lat, lon) 
			
GMAPS_URL =  "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmaps_img(points):
	markers = '&'.join('markers=%s,%s' % (p.lat,  p.lon) for p in points)
	return GMAPS_URL + markers

class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	coords = db.GeoPtProperty()

class MainPage(Handler):
	def render_front(self, title="", art="", error=""):
		arts = db.GqlQuery("SELECT * FROM Art "
						   "ORDER BY created DESC")

		#prevent the running of multiple queries
		arts = list(arts)

		points = filter(None, (a.coords for a in arts))
		img_url = None
		if points:
			img_url = gmaps_img(points)

		self.render("front.html", title = title, art = art, error = error, arts = arts, img_url = img_url)

	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")
	
		if art and title:
			a = Art(title = title, art = art)
			coords = getCoords(self.request.remote_addr)
			if coords:
				a.coords = coords			
			a.put()
			self.redirect("/")
		else:
			error = "we need both a title and some artwork!!!"
			self.render_front(title, art, error)

app = webapp2.WSGIApplication([('/', MainPage)], 
								debug = True)
