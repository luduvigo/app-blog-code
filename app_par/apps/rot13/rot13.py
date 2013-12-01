import webapp2

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
