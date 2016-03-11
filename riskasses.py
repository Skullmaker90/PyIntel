#!/usr/bin/python

import libs.Km
import libs.Zkb
import libs.Who
import libs.Logging

log = libs.Logging.Log('Risk_log')
zkb = libs.Zkb.Zkb()
who = libs.Who.Who()

def check_cyno(pilot):
  cyno_ids = [21096, 28646]
  log.debug('Retriving pilot ID')
  pilot_id = int(who('character', 'name', pilot)['info']['character_id'])
  log.debug('Pilot ID: %s' % (pilot_id))
  log.debug('Retrieving Losslist.')
  rec_loss_list = zkb.query(fmod = ['characterID', pilot_id],
                            ftypemod = ['losses'],
                            ptlmod = ['limit', 100])
  log.debug('Losslist retrieved, Length: %s' % (len(rec_loss_list)))
  log.debug('Mapping Km build_objects.')
  rec_loss_list = map(build_object, rec_loss_list)
  log.debug('Map complete, Returning filter result.')
  return filter(itemid_comp, rec_loss_list)

def build_object(km):
  return libs.Km.Killmail(km)

def itemid_comp(kmobj):
  iscyno = False
  cyno_ids = [21096, 28648]
  for item in kmobj.items.highs:
    if cyno_ids.count(int(item['typeID'])) >= 1:
      iscyno = True
  for item in kmobj.items.cargo:
    if cyno_ids.count(int(item['typeID'])) >= 1:
      iscyno = True
  return iscyno
