import hashlib
import hmac
import random
import string

################################
# Utilities

SECRET = 'imsosecretppzz'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=None):
    if salt is None:
        salt = make_salt()
    return "%s,%s" % (hashlib.sha256(name + pw + salt).hexdigest(),salt)

def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

################################
