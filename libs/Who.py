import requests
import threading
import logging
import re
import time
import multiprocessing
from Logging import Log
from urlparse import urlparse, urlunparse, parse_qsl

logs = Log('Who')
cache_re = re.compile(r'max-age=([0-9]+)')

class APIException(Exception):
  logs.warning('Exception Passed: %s' % (Exception))
  pass

class Cache(object):
  def __init__(self):
    self.dct = {}

  def get(self, item):
    return self.dct.get(item, None)

  def insert(self, item, value):
    self.dct[item] = value

  def remove(self, item):
    self.dct.pop(item, None)

class APIConnection(object):
  def __init__(self, add_headers=None, user_agent=None):
    """ Construct session. """
    ses = requests.Session()
    if not add_headers:
      add_headers = {}
    if not user_agent:
      user_agent = "PyIntel 0.1"
    ses.headers.update({
      "User-agent": user_agent,
      "Accept": "application/json",
    })
    ses.headers.update(add_headers)
    self._ses = ses
    self.cache = Cache()

  def chkCache(self, asset, params):
    """ Retreive cached assets if present. """
    key = (asset,
        frozenset(self._ses.headers.items()), 
        frozenset(params.items()))
    cached = self.cache.get(key)
    if cached and cached['expires'] > time.time():
      logs.debug('Asset cached: %s, %s' % (asset, params))
      return cached['payload']
    elif cached:
      logs.debug('Asset cached but expired: %s, %s' % (asset, params))
      self.cache.remove(key)

  def get(self, asset, params=None):
    """ Get session request. If 200, return json and cache if needed. """
    if not params:
      params = {}
    parsed = urlparse(asset)
    asset = urlunparse(parsed._replace(query=''))
    qs = parsed.query
    _vars = {}
    for tup in parse_qsl(qs):
      _vars[tup[0]] = tup[1]
    for key in params:
      _vars[key] = params[key]
    self.chkCache(asset, _vars)
    r = self._ses.get(asset, params=_vars)
    if r.status_code != 200:
      raise APIException("Unexpected Status Code %s" % (r.status_code))
    res = r.json()
    key = (asset, frozenset(self._ses.headers.items()), frozenset(_vars.items()))
    exp = self._get_exp(r)
    if exp > 0:
      self.cache.insert(key, {'expires': time.time() + exp, 'payload': res})
    return res

  def _get_exp(self, response):
    """ Get experation for cache item."""
    if 'Cache-Control' not in response.headers:
      return 0
    if any([s in response.headers['Cache-Control'] for s in ['no-cache', 'no-store']]):
      return 0
    match = cache_re.search(response.headers['Cache-Control'])
    if match:
      return int(match.group(1))
    return 0

class Consumer(multiprocessing.Process):
  def __init__(self, tq, rq):
    """ Meta class for mul_call consumers. """
    multiprocessing.Process.__init__(self)
    self.tqueue = tq
    self.rqueue = rq

  def run(self):
    """ Get and complete item from tqueue. """
    name = self.name
    while True:
      next_task = self.tqueue.get()
      if next_task is None:
        self.tqueue.task_done()
        break
      a = next_task()
      self.tqueue.task_done()
      self.rqueue.put(a)

class InitClass(object):
  def __init__(self, a, b, c):
    """ Metaclass for mul_call workers. Passed params. """
    self._type = a
    self._arg = b
    self._var = c

  def __call__(self):
    who = Who()
    return who(self._type, self._arg, self._var)

class Who(APIConnection):
  def __init__(self):
    self._endpoint = "http://evewho.com/api.php"
    self._cache = {}
    self._params = None
    self.data = {}
    APIConnection.__init__(self)

  def __call__(self, _type, _arg, _var, page=None, force=None):
    """Evewho lookup for Toons, Corps, Alliances.

    Keyword arguments:
    _type -- Type of lookup. (character, corp, corplist, alliance, allilist)
    _arg -- Matching pattern. (name, id)
    _var -- Pattern to be matched. (Tali Lyrae, 684719410)
    """
    params = {'type': _type, _arg: _var, 'page': page}
    if params is not self._params or force is True:
      self._params = params
      self.data = self.get(self._endpoint, self._params)
      self._chkmem()
    return self.data

  def _chkmem(self):
    """ Check if corplist, alliance, > 200 members, get all if so."""
    if self.data['info'].has_key('memberCount'):
      for i in range(1, (int(self.data['info']['memberCount']) / 200 + 1)):
        self._params['page'] = i
        r = self.get(self._endpoint, self._params)
        self.data['characters'] += r['characters']

  def mul_call(self, joblist):
    """ Takes list of Who().__call__, Place into queue, return all. """
    who = Who()
    t = multiprocessing.JoinableQueue()
    r = multiprocessing.Queue()
    n_con = multiprocessing.cpu_count()
    consumers = [ Consumer(t, r) for i in xrange(n_con) ]
    ntasks = len(joblist)
    for w in consumers:
      w.start()
    for job in joblist:
      t.put(InitClass(job[0], job[1], job[2]))
    # This is to kill Consumers
    for i in xrange(n_con):
      t.put(None)
    t.join()
    self.data = {}
    while ntasks:
      result = r.get()
      self.data[result['info']['name']] = result
      ntasks -= 1
    return self.data
