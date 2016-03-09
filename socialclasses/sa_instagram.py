import json
import requests
import keys
import datetime

class Instagram:

	def getHashtag(self, hashtag):
		url = "https://api.instagram.com/v1/tags/" + hashtag + "/media/recent?access_token=" + keys.INSTAGRAM_ACCESS_TOKEN

		r = requests.get(url)
		content = r.text
		content_dict = json.loads(content)
		data = content_dict['data']

		temp_list = {}
		for d in data:
			k_raw = datetime.datetime.fromtimestamp(int(d['caption']['created_time']))

			k = str(k_raw.strftime('%Y%m%d%H%M%S'))
			k2 = int(k + '2')

			temp_list_inner = {
							"text" : d['caption']['text'],
							"likes" : int(d['likes']['count']),
							"user" : {
									"name" : d['caption']['from']['username'],
									"image" : d['caption']['from']['profile_picture'],
									},
							"datetime" : str(k_raw.strftime('%Y-%m-%d : %H-%M-%S')),
							"url" : d['link'],
							"from" : "instagram",
							"media" : {
								"photo" : d['images']['standard_resolution']['url'],
								"photo_link" : d['link']
							}
			}

			temp_list[k2] = temp_list_inner

		return json.dumps(temp_list)



		