#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
import HTMLParser
import htmllib

def escape_html(s):
    return cgi.escape(s, quote = True)

def html_decode(s):
	html_parser = HTMLParser.HTMLParser()
	return html_parser.unescape(s)

#form = """
#<form method="post">
#	What is your birthday?
#	<br>
#	<label> Day <input type="text" name="day" value="%(day)s"><label>
#	<label>	Month <input type="text" name="month" value="%(month)s"> <label>
#	<label> Year <input type="text" name="year" value="%(year)s"> <label>
#	<div style="color: red">%(error)s</div>	
#	<br>
#	<br>
#	<input type= "submit">
#</form>
#	"""

#months = ['January',
#          'February',
#          'March',
#          'April',
#          'May',
#          'June',
#          'July',
#          'August',
#          'September',
#          'October',
#          'November',
#          'December']
#
#def valid_month(month):
#	if month:
#		cap_month = month.capitalize()
#		if cap_month in months:
#			return cap_month
#
#def valid_day(day):
#    if day and day.isdigit():
#        num = int(day)
#        if num in range(1,32):
#            return num

#def valid_year(year):
#    if year and year.isdigit():
#        year = int(year)
#        if year >= 1900 and year <= 2020:
#            return year

#class MainPage(webapp2.RequestHandler):
#	def write_form(self, error="", month="", day="", year=""):
#		self.response.out.write(form % {"error": error, "month": month, "day": day, "year": year})		

# 	def get(self):
#		self.write_form()

#	def post(self):
#		user_month = self.request.get('month')
#		user_day = self.request.get('day')
#		user_year = self.request.get('year')
#		month = valid_month(user_month)
#		day = valid_day(user_day)
#		year = valid_year(user_year)
#		if not(month and day and year):
#			self.write_form("That doesn't look valid to me, friend.", user_month, user_day, user_year)
#		else:
#			self.response.out.write("Thanks! That's a totally valid day!")


#app = webapp2.WSGIApplication([('/', MainPage)],
#                              debug=True)

def rotate13(s):
	result = ""
	for a in s:
		if re.match("[A-Z]", a):
			att = (((ord(a) - 65) + 13)% 26) + 65
			a = chr(att)
		if re.match("[a-z]", a):
			att = (((ord(a) - 97) + 13)% 26) + 97
			a = chr(att)
		result += a
	return result

form="""
<form method="get"> 
	What is your birthday?
	<br>
	<input type="text" name="day">
	<input type="text" name="month">	
	<input type="text" name="year">
	<br>
	<br>
	<input type= "submit">
</form>"""

formRot13="""

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(content)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""
def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    # this has to be last:
    s = s.replace("&amp;", "&")
    return s

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Hello, Udacity!")	

class Rot13(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(formRot13 % {"content": ""})
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		originalInput = self.request.get('text')
		output = rotate13(originalInput)
		output_un = escape_html(output)
		self.response.out.write(formRot13 % {"content": output_un})

app = webapp2.WSGIApplication([('/', MainPage),('/rot13',Rot13)],
								debug=True)		


