import os
from pprint import pprint
from cache import Cache

hashtags = os.listdir('hashtags')

for h in hashtags:
	if h.startswith("."):
		continue

	pprint(h)
	c = Cache(h)
	c.buildIt()
