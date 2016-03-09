#!/usr/bin/env python3
import keys
from cache import Cache
from flask import Flask, request
APP = Flask(__name__)

if keys.IS_PRODUCTION:
	APP.debug = True

@APP.route("/")
def hello():
	return "test"


@APP.route("/hashtag/<input_hashtag>")
def hash_t(input_hashtag):

	c = Cache(input_hashtag)
	cc = c.buildIt()
	cr = c.readIt()

	return cr



if __name__ == "__main__":
	APP.run()
