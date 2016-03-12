#!/usr/bin/python

import libs.Km
import libs.Zkb
import libs.Who
import libs.Logging

log = libs.Logging.Log('Risk_log')
zkb = libs.Zkb.Zkb()
who = libs.Who.Who()

def check_cyno(name, limit=100):
  log.debug('Retriving pilot ID')
  pilot_id = int(who('character', 'name', name)['info']['character_id'])
  log.debug('Retrieving Losslist.')
  pilot_loss_list = zkb.query(fmod = ['characterID', pilot_id],
                            ftypemod = ['losses'],
                            ptlmod = ['limit', limit])
  log.debug('Mapping Km build_objects.')
  pilot_loss_list = map(build_object, pilot_loss_list)
  log.debug('Map complete, Returning filter result.')
  return filter(itemid_comp, pilot_loss_list)

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

def check_doctorine(name):
  pilot_id = int(who('character', 'name', pilot)['info']['character_id'])

  def compare_items(kmobj):
    key_match = ['highs', 'mids', 'lows']
    for k, v in kmobj.items():
      if key_match.count(k) == 1:
        pass
