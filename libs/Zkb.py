import requests
requests.packages.urllib3.disable_warnings()

class Zkb(object):
  def __init__(self):
    self.url = 'https://zkillboard.com/api/'
    self.ptlmod = ['/limit/', '/page/', '/startTime/',
      '/endTime/', '/year/', '/month/',
      '/beforeKillID/', '/afterKillID/',
      '/pastSeconds/', '/killID/']
    self.ftypemod = ['/kills/', '/losses/',
      '/w-space/', '/solo/']
    self.omod = ['/orderDirection/asc/',
      '/orderDirection/desc/']
    self.fmod = ['/characterID/', '/corporationID/', '/allianceID/',
      '/factionID/', '/shipTypeID/', '/groupID/',
      '/solarSystemID/', '/regionID/', '/warID/']
    self.imod = ['/no-items/', '/no-attackers/']

  def build_url(self, keydict):
    url = self.url
    for key in keydict:
      if keydict[key] != None:
        if eval('self.%s' % (key)).count('/' + keydict[key][0] + '/'):
          for value in keydict[key]:
            url = url + str(value) + '/'
    return url

  def query(self, ptlmod=None, ftypemod=None, omod=None, fmod=None, imod=None):
    moddict = {'ptlmod': ptlmod, 'ftypemod': ftypemod, 'omod': omod, 'fmod':fmod}
    url = self.build_url(moddict)
    headers = {'user-agent': 'https://init1.us/', 'Maintainer': 'Anthony Smith asmith@cari.net', 'Accept-Encoding': 'gzip'}
    res = requests.get(url).json()
    r = []
    for kill in res:
      r.append(Killmail(kill))
    return r

class items(object):
  def __init__(self):
    self.high = []
    self.mid = []
    self.low = []
    self.cargo = []

  def _populate(self, itemlist):
    for item in itemlist:
      

class Killmail(items):
  def __init__(self, km):
    self.killID = km['killID']
    self.killTime = km['killTime']
    self.zkb = km['zkb']
    self.attackers = km['attackers']
    self.victim = km['victim']
    self.items = km['items']
    self.solarSystemID = km['solarSystemID']
    self.moonID = km['moonID']
