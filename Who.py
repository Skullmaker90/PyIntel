import requests
import threading
import logging
import re
import time
from urlparse import urlparse, urlunparse, parse_qsl

logger = logging.getLogger("PyIntel.Who")
cache_re = re.compile(r'max-age=([0-9]+)')

class APIException(Exception):
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
    key = (asset, 
        frozenset(self._ses.headers.items()), 
        frozenset(params.items()))
    cached = self.cache.get(key)
    if cached and cached['expires'] > time.time():
      logger.debug('Match for asset %s (params=%s)', asset, params)
      return cached['payload']
    elif cached:
      logger.debug('Expired state for asset %s (params=%s)', asset, params)
      self.cache.remove(key)
    else:
      logger.debug('Missing asset %s (params=%s)', asset, params)

  def get(self, asset, params=None):
    logger.debug('Recieve asset %s' % (asset))
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
    logger.debug('Recieveing asset %s (params=%s)', asset, _vars)
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
    if 'Cache-Control' not in response.headers:
      return 0
    if any([s in response.headers['Cache-Control'] for s in ['no-cache', 'no-store']]):
      return 0
    match = cache_re.search(response.headers['Cache-Control'])
    if match:
      return int(match.group(1))
    return 0

class Who(APIConnection):
  def __init__(self):
    self._endpoint = "http://evewho.com/api.php"
    self._cache = {}
    self._params = {}
    self._threads = []
    self.data = None
    APIConnection.__init__(self)

  def __call__(self, _type, _arg, _var, page=None, force=None):
    params = {'type': _type, _arg: _var, 'page': page}
    if not (params == self._params and force is not True):
      self._params = params
      t = WhoQ(self._endpoint, params)
      self.data = self.get(self._endpoint, params)
      self._chkmem()
    return self.data

  def _chkmem(self):
    if self.data['info'].has_key('memberCount'):
      for i in range(1, (int(self.data['info']['memberCount']) / 200 + 1)):
        self._params['page'] = i
        r = self.get(self._endpoint, self._params)
        self.data['characters'] += r['characters']

class WhoQ(threading.Thread):
  def __init__(self, uri, params):
    threading.Thread.__init__(self)
    self.uri = uri
    self.params = params

  def run(self):
    r = APIConnection.get(self.uri, params)
    return r
