#!/usr/bin/python

class Killmail(object):
  def __init__(self, km):
    self.kill_id = km['killID']
    self.kill_time = km['killTime']
    self.km_value = km['zkb']['totalValue']
    self.attackers = km['attackers']
    self.victim = km['victim']
    self.items = Items(km['items'])
    self.position = km['position']
    self.solar_system_id = km['solarSystemID']
    self.moon_id = km['moonID']

  def time(self):
    return self.kill_time

class Items(Killmail):
  def __init__(self, itemlist):
    self.highs = []
    self.mids = []
    self.lows = []
    self.drones = []
    self.rigs = []
    self.subsystems = []
    self.cargo = []
    self._populateitems(itemlist)

  def __call__(self):
    r = {'highs': self.highs, 'mids': self.mids,
        'lows': self.lows, 'drones': self.drones,
        'rigs': self.rigs, 'cargo': self.cargo}
    if self.subsystems:
      r['subsystems'] = self.subsystems
    return r

  def _populateitems(self, itemlist):
    for item in itemlist:
      flag = item['flag']
      if flag in range(11, 19):
        self.lows.append(item)
      elif flag in range(19, 27):
        self.mids.append(item)
      elif flag in range(27, 35):
        self.highs.append(item)
      elif flag is 87:
        self.drones.append(item)
      elif flag in range(92, 95):
        self.rigs.append(item)
      elif flag in range(125, 130):
        self.subsystems.append(item)
      else:
        self.cargo.append(item)
