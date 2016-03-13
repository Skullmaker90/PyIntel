#!/usr/bin/python

import libs.Km
import libs.Zkb
import libs.Who
import libs.Logging

log = libs.Logging.Log('Risk_log')
zkb = libs.Zkb.Zkb()
who = libs.Who.Who()

def set_log_state(state):
  log.set_log_state(state)

class Pilot(object):
  def __init__(self):
    self.data = {}

  def put(self, key, item):
    self.data[key] = item

  def get(self, key):
    return self.data[key]

  def pop(self, key):
    return self.data.pop(key)

def check_cyno(pilot, limit=100):
  log.info('Storing pilot name/limit: %s/%s' % (pilot.get('name'), limit))
  log.info('Retriving pilot ID')
  pid = int(who('character', 'name', pilot.get('name'))['info']['character_id'])
  pilot.put('id', pid)
  log.info('Retrieving Losslist.')
  loss_list = zkb.query(fmod = ['characterID', pilot.get('id')],
                            ftypemod = ['losses'],
                            ptlmod = ['limit', limit])
  log.info('Mapping Km build_objects.')
  loss_obj_list = map(build_object, loss_list)
  pilot.put('losses', loss_obj_list)
  log.info('Map complete, Returning filter result.')
  return filter(itemid_comp, loss_obj_list)

def build_object(km):
  return libs.Km.Killmail(km)

def itemid_comp(kmobj):
  is_cyno = False
  cyno_ids = {'Cynosural Field Generator': 21096,
              'Covert Cynosural Field Generator': 28648}
  highs = kmobj.items.highs
  cargo = kmobj.items.cargo
  for item in (highs + cargo):
    if item['typeID'] in cyno_ids.values():
      is_cyno = True
  return is_cyno

def check_doctorine():
  pass

def main(name):
  pilot = Pilot()
  pilot.put('name', name)
  return pilot
