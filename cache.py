import os
import json
import datetime
from collections import OrderedDict
from apis import instagram, twitter
from pprint import pprint
import datetime as dt

class Cache(object):
	def __init__(self, hashtag):

		if '#' in hashtag:
			self.hashtag = hashtag.replace('#','')
		else:
			self.hashtag = hashtag

		a_path = os.path.dirname(os.path.abspath(__file__))
		self.hash_root_path = a_path + "/hashtags"
		self.hash_path = self.hash_root_path + "/" + self.hashtag
		self.instagram_file_name = "instagram.json"
		self.twitter_file_name = "twitter.json"
		self.file_name = "cache.json"
		self.instagram_file_path = self.hash_path + "/" + self.instagram_file_name
		self.twitter_file_path = self.hash_path + "/" + self.twitter_file_name
		self.file_path = self.hash_path + "/" + self.file_name
		self.time = dt.datetime.now()
		self.mod_intv = self.time - dt.timedelta(minutes=14)


	def readIt(self, **kwargs):
		read = {}
		with open(self.file_path, "r+") as f:
			raw = f.read()
		"""
		if kwargs['rt'] == False:
			for r in json.loads(raw):
				if r['text'].startswith("RT "):
					continue
				raw.append(r)
		"""

		read = raw

		return read
		

	def buildIt(self):

		if not os.path.exists(self.hash_path):
			os.makedirs(self.hash_path)

		if os.path.exists(self.file_path):
			self._checkMod(self.file_path)

		self._twitterBuild()
		self._instagramBuild()

		self._fileHousekeeping(self.file_path)

		combo = {}
		with open(self.twitter_file_path, "r+") as f:
			combo.update(json.loads(f.read()))

		with open(self.instagram_file_path, "r+") as f:
			combo.update(json.loads(f.read()))

		combo_ordered = OrderedDict(sorted(combo.items(), reverse=True))
		combo_json = json.dumps(combo_ordered)

		
		with open(self.file_path, "w+") as fw:
			fw.write(combo_json)
		
		return

	def _twitterBuild(self):

		self._fileHousekeeping(self.twitter_file_path)

		new = twitter.getHashtag(self.hashtag)

		#pprint("build twitter fired")

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


	def _instagramBuild(self):

		self._fileHousekeeping(self.instagram_file_path)

		new = instagram.getHashtag(self.hashtag)

		#pprint("build instagram fired")

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

	def _checkMod(self, path):
		"""
			This function will return False if the file was 
			modified within the mod_intv.
		"""

		st = os.stat(path)    
		mtime = dt.datetime.fromtimestamp(st.st_mtime)
		if mtime > self.mod_intv:
			#pprint("DID NOT MOD")
			return

		#pprint("DID MOD***********")
		return

	def _fileHousekeeping(self, path):
		# Check to see if file exists
		if not os.path.exists(path):
			#pprint("make file")
			# Create file if it does not exist
			with open(path, "w+") as fr:
				pass

	
