import os
import time
import Who
from datetime import datetime

class _Dict(object):
  def __init__(self):
    self._data = {}

  def _get(self, key):
    return self._data[key]

  def _set(self, key, value):
    self._data[key] = value

  def _rm(self, key):
    self._data.pop(key)

class altfind(object):
  def __init__(self):
    self._info = _Dict()
    self._history = []
    self._tmp = []
    self.who = Who.Who()
    self.alts = _Dict()

  def search(self, data):
    self._populate(data)
    self._filterhist()
    self._itertime(self._history)
    for corp in self._history:
      self._tmp.append(self.who('corplist', 'id', corp['corporation_id']))

  def _populate(self, data):
    for k, v in data['info'].iteritems():
      self._info._set(k, v)
    self._history = data['history']

  def _itertime(self, resource):
    for item in resource:
      for k, v in item.iteritems():
        if (k == 'end_date' or k == 'start_date'):
          item[k] = self._settime(v)

  def _settime(self, source):
    if source:
      _format = '%Y-%m-%d %H:%M:%S'
      return datetime.strptime(source, _format)

  def _filterhist(self):
    for corp in self._history:
      if (int(corp['corporation_id']) < 1000182 and int(corp['corporation_id']) > 1000002):
        self._history.remove(corp)
