import json
import datetime
import requests
import keys
import oauth2
from pprint import pprint


class Twitter:
	def __init__(self):
		pass

	def getHashtag(self, hashtag):
		if '#' not in hashtag:
			hashtag = '%23' + hashtag
		else:
			hashtag.replace('#', '%23')

		base_url_raw = "https://api.twitter.com/1.1/search/tweets.json?q=" + hashtag
		base_url = base_url_raw.encode("utf-8")
			
		consumer = oauth2.Consumer(key=keys.TWITTER_CONSUMER_KEY, secret=keys.TWITTER_CONSUMER_SECRET)
		token = oauth2.Token(key=keys.TWITTER_ACCESS_KEY, secret=keys.TWITTER_ACCESS_SECRET)		
		client = oauth2.Client(consumer, token)
		b = "".encode("utf-8")
		resp, content = client.request(base_url, method="GET", body=b, headers=None)
		content_decode = json.loads(content.decode("utf-8"))
		tweets = content_decode['statuses']		

		temp_list = {}
		for tweet in tweets:
			if tweet['lang'] != "en":
				continue

			k_raw = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')

			k = str(k_raw.strftime('%Y%m%d%H%M%S'))
			k1 = int(k + '1')
			temp_list_inner = {
							"text" : tweet['text'],
							"likes" : int(tweet['favorite_count']),
							"user" : {
									"name" : tweet['user']['screen_name'],
									"image" : tweet['user']['profile_image_url'],
									},
							"datetime" : str(k_raw.strftime('%Y-%m-%d : %H-%M-%S')),
							"url" : "",
							"from" : "twitter",
							"media" : ""
			}
			"""
			TODO: add in url fields
			"""


			if not tweet['entities'].get('media'):
				tweet['entities']['media'] = list()

			for m in tweet['entities']['media']:
				
				if m['type'] != "photo":
					continue
			
				temp_list_inner['media'] = {
									"photo" : m['media_url'],
									"photo_link" : m['display_url']
				}

			temp_list[k1] = temp_list_inner
		
		return json.dumps(temp_list)
