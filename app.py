#!/usr/bin/env python3
import keys
from cache import Cache
from flask import Flask, request
APP = Flask(__name__)

if keys.IS_PRODUCTION:
	APP.debug = True

TEST_POST_PASS = "8392hfuehf934fn93f2dj20djw0d92"

@APP.route("/")
def hello():
	return "test"


@APP.route("/hashtag/<input_hashtag>", methods=['POST'])
def hash_t(input_hashtag):
	if request.form['api_key'] == TEST_POST_PASS:
		c = Cache(input_hashtag)
		cc = c.buildIt()
		cr = c.readIt()

		return cr
	else:
		return 403



if __name__ == "__main__":
	APP.run('0.0.0.0')
