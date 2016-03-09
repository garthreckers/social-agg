import os
import json
import datetime
from collections import OrderedDict
from socialclasses.sa_twitter import Twitter
from socialclasses.sa_instagram import Instagram
from pprint import pprint
import datetime as dt

class Cache(object):
	def __init__(self, hashtag):

		if '#' in hashtag:
			self.hashtag = hashtag.replace('#','')
		else:
			self.hashtag = hashtag

		self.hash_root_path = "hashtags"
		self.hash_path = self.hash_root_path + "/" + self.hashtag
		self.instagram_file_name = "instagram.json"
		self.twitter_file_name = "twitter.json"
		self.file_name = "cache.json"
		self.instagram_file_path = self.hash_path + "/" + self.instagram_file_name
		self.twitter_file_path = self.hash_path + "/" + self.twitter_file_name
		self.file_path = self.hash_path + "/" + self.file_name
		self.time = dt.datetime.now()
		self.mod_intv = self.time - dt.timedelta(minutes=1)


	def readIt(self):
		read = ""
		with open(self.file_path, "r+") as f:
			read = f.read()

		return read
		

	def buildIt(self):

		if not os.path.exists(self.hash_path):
			os.makedirs(self.hash_path)

		self.twitterBuild()
		self.instagramBuild()

		fileHousekeeping(self.file_path)

		combo = {}
		with open(self.twitter_file_path, "r+") as f:
			combo.update(json.loads(f.read()))

		with open(self.instagram_file_path, "r+") as f:
			combo.update(json.loads(f.read()))

		combo_ordered = OrderedDict(sorted(combo.items(), reverse=True))
		combo_json = json.dumps(combo_ordered)

		if self.checkMod(self.file_path):

			with open(self.file_path, "w+") as fw:
				fw.write(combo_json)
		
		return

	def twitterBuild(self):

		self.fileHousekeeping(self.twitter_file_path)

		twit = Twitter()
		new = twit.getHashtag(self.hashtag)

		pprint("build twitter fired")

		old = None
		
		with open(self.twitter_file_path, "r+") as fr:
			o_read = fr.read()
			if o_read is not "":
				old = json.loads(o_read)

		with open(self.twitter_file_path, "w+") as fw:
			data = None
			if old:
				data = json.loads(new)
				data.update(old)
				data = json.dumps(data)
			else:
				data = new

			fw.write(data)

		return


	def instagramBuild(self):

		self.fileHousekeeping(self.instagram_file_path)

		instagram = Instagram()
		new = instagram.getHashtag(self.hashtag)

		pprint("build instagram fired")

		old = None
		
		with open(self.instagram_file_path, "r+") as fr:
			o_read = fr.read()
			if o_read is not "":
				old = json.loads(o_read)

		with open(self.instagram_file_path, "w+") as fw:
			data = None
			if old:
				#pprint(new)
				data = json.loads(new)
				data.update(old)
				data = json.dumps(data)
			else:
				data = new
			fw.write(data)

		return

	def checkMod(self, path):
		"""
			This function will return False if the file was 
			modified within the mod_intv.
		"""

		st = os.stat(path)    
		mtime = dt.datetime.fromtimestamp(st.st_mtime)
		if mtime > self.mod_intv:
			pprint("DID NOT MOD")
			return False

		pprint("DID MOD***********")
		return True

	def fileHousekeeping(self, path):
		# Check to see if file exists
		if not os.path.exists(path):
			pprint("make file")
			# Create file if it does not exist
			with open(path, "w+") as fr:
				pass

	
