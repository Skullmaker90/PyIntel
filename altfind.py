import os
import time
import libs.Who
from libs.Logging import Log
from datetime import datetime, timedelta

who = libs.Who.Who()

class CharObject(object):
  def __init__(self, char):
    self.characterid = char['info']['character_id']
    self.name = char['info']['name']
    self.corpid = char['info']['corporation_id']
    self.history = char['history']
    self.history_id_list = list(c['corporation_id'] for c in char['history'])

  def get_hist_attr(self, attr):
    for corp in self.history:
      return corp[attr]

class HistCorpObject(object):
  def __init__(self, corpobj):
    self.corpid = corpobj['corporation_id']
    self.start_date = corpobj['start_date']
    self.end_date = corpobj['end_date']

def search(name):
  r = who('character', 'name', name)
  pilot = CharObject(r)
  pilot.history = filter_hist(pilot.history)
  corp_joblist = map(get_joblist, pilot.history)
  corp_charlist = who.mul_call(corp_joblist)
  char_joblist = map(get_charlist, filter_id(list(corp_charlist.values())))
  altlist = who.mul_call(char_joblist)
  for alt in altlist.values():
    alt['history'] = filter_hist(alt['history'])
  filter_corp_match(pilot.history_id_list, altlist)
  final_list = get_delta(pilot.history, altlist)
  for i in range(5):
    for item in final_list:
      if item['info']['name'] == pilot.name:
        final_list.pop(final_list.index(item))
  return final_list

def set_ts(item):
  _format = '%Y-%m-%d %H:%M:%S'
  item['start_date'] = datetime.strptime(item['start_date'], _format)
  if item['end_date'] is not None:
   item['end_date'] = datetime.strptime(item['end_date'], _format)
  return item

def filter_hist(hist_list):
  map(set_ts, hist_list)
  hist_list = filter(pop_npc, hist_list)
  return hist_list

def pop_npc(item):
  return (int(item['corporation_id'])) > 1000182

def filter_pilot_history(pilot_hist):
  return pilot_hist_item['corporation_id'] == pilot_history

def get_joblist(corpitem):
  return ['corplist', 'id', int(corpitem['corporation_id'])]

def get_charlist(charitem):
  return ['character', 'id', int(charitem)]

def get_delta(pilot_hist, altlist):
  nlist = []
  for pilot in altlist.values():
    for corp in pilot['history']:
      corp_id = corp['corporation_id']
      start_date = corp['start_date']
      end_date = corp['end_date']
      for item in pilot_hist:
        itemid = item['corporation_id']
        itemstart = item['start_date']
        itemend = item['end_date']
        if corp_id == itemid:
          if ((itemstart - start_date < timedelta(1)) and (start_date - itemstart < timedelta(1))):
            print (itemstart - start_date)
            nlist.append(pilot)
          elif end_date != None:
            try: 
              if ((itemend - end_date < timedelta(1)) and (end_date - itemend < timedelta(1))):
                print (itemend - end_date)
                nlist.append(pilot)
            except:
              pass
  return nlist

def filter_id(altlist):
  idlist = []
  for corp in altlist:
    for toon in corp['characters']:
      if type(toon) is dict:
        idlist.append(int(toon['character_id']))
  return idlist

def filter_corp_match(pilot_corpid_list, alt_list):
  for pilot in alt_list.values():
    nlist = []
    for corp in pilot['history']:
      try: 
        pilot_corpid_list.index(corp['corporation_id'])
        nlist.append(corp)
      except: 
        pass
    pilot['history'] = nlist
