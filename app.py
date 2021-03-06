#!/usr/bin/env python3
import keys
from cache import Cache
from flask import Flask, request
APP = Flask(__name__)

if not keys.IS_PRODUCTION:
	APP.debug = True

TEST_POST_PASS = "8392hfuehf934fn93f2dj20djw0d92"

@APP.route("/")
def hello():
	return "test"


@APP.route("/hashtag/<input_hashtag>", methods=['POST', 'GET'])
def hash_t(input_hashtag):
	"""
	When ready to go live, uncomment this section and remove GET from the methods
	if request.form['api_key'] == TEST_POST_PASS:
		c = Cache(input_hashtag)
		cc = c.buildIt()
		cr = c.readIt()

		return cr
	else:
		return 403

	... and delete this stuff below
	"""

	c = Cache(input_hashtag)
	cc = c.buildIt()
	cr = c.readIt()

	return cr



if __name__ == "__main__":
	APP.run(host='0.0.0.0')
