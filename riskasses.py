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

def get_items(pilotobj, name, limit=100):
  log.info('Pilot name/limit:  %s/%s' % (name, limit))
  pilotobj.put('name', name)
  log.info('Retrieving ID.')
  pilot_id = int(who('character', 'name', pilotobj.get('name'))['info']['characterID'])
  log.info('%s ID: %s' % (name, pilot_id))
  pilotobj.put('id', pilot_id)
  log.info('Retriving Losses.')
  pilot_losses = get_ent_losses(pilotobj, 'characterID', pilot_id, limit)
  pilotobj.put('losses', pilot_losses)
  pilot_corp_losses = get_ent_losses(pilotobj, 'corporationID', pilot_losses[0]\
                                                                ['victim']\
                                                                ['corporationID'])
  pilotobj.put('corp_losses', pilot_corp_losses)
  return pilotobj

def get_ent_losses(pilotobj, idtype, _id, limit=100):
  log.info('Retriving killmails: %s/%s' % (pilotobj.get('name'), limit))
  losses = zkb.query(fmod = [idtype, _id],
                      ftypemod = ['losses'],
                      ptlmod = ['limit', limit])
  log.info('Objectifing losses (Sorry).')
  losses = map(build_obj, losses)
  return losses

def check_cyno(pilotobj):
  losses = pilotobj.get('losses')
  return filter(itemid_comp, losses)

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

def check_doctorine(pilotobj, limit=100):
  doc_list = []
  losses = pilotobj.get('losses')
  corp_losses = pilotobj.get('corp_losses')
  pairs = zip(losses, corp_losses)
  for item in pairs:
    kms = []
    _id = item['victim']['shipTypeID']
    sim_km = next((ent for ent in pairs if ent['id'] == _id), None)
    if sim_km:
      for cls_method in item.items.__dict__:
        pass
    

def main(name):
  if isinstance(name, (str, unicode)):
    pilot = Pilot()
    pilot.put('name', name)
    return pilot
  raise TypeError("Passed '%s' not str" % (name))
