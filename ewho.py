import requests

class who():
	def __init__(self):
		self.url = 'http://evewho.com/api.php?type=%s&%s=%s'
		#self.ptype = ['corplist', 'allilist', 'character', 'corporation', 'alliance']
		#self.rdict = {'corplist': [

	def query(self, ptype, match, var):
		print(self.url % (ptype, match, var))
		r = requests.get(self.url % (ptype, match, var))
		return r.json()

	#def corplist(self, match, var):
	#	r = requests.get(self.url % (ptype[0], match, var))
	#	return r.json()
	
	#def allilist(self):
	#	r = self.url[:31] + self.ptype[1])
	#	return r.json()

	#def character(self, match, var):
	#	r = requests.get(self.url % (self.ptype[2], match, var))
	#	return r.json()

	#def corporation(self, match, var):
	#	r = requests.get(self.url % (self.ptype[3], match, var))
	#	return r.json()

	#def alliance(self, match, var):
	#	r = requests.get(self.url % (self.ptype[4], match, var))
	#	return r.json()
