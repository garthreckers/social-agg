#!/usr/bin/python3
import os
from pprint import pprint
from cache import Cache

abpath = os.path.dirname(os.path.abspath(__file__))
hashtags = os.listdir(abpath + '/hashtags')

for h in hashtags:
	if h.startswith("."):
		continue

	pprint(h)
	c = Cache(h)
	c.buildIt()
