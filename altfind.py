import os
import time
import libs.Who
from libs.Logging import Log
from datetime import datetime

def altfind(pilot_name):
  search(pilot_name)

def search(pilot):
  who = libs.Who.Who()
  r = who('character', 'name', pilot)
  pilot_history = r['history']
  filtered_list = filter(filter_history, pilot_history)
  time_set_list = map(set_timestamp, filtered_list)
  joblist = map(get_joblist, time_set_list)
  pos_altlist = who.mul_call(joblist)

def set_timestamp(item):
  _format = '%Y-%m-%d %H:%M:%S'
  item['start_date'] = datetime.strptime(item['start_date'], _format)
  if item['end_date'] is not None:
   item['end_date'] = datetime.strptime(item['end_date'], _format)
  return item

def filter_history(corp):
  return (int(corp['corporation_id'])) > 1000182

def get_joblist(corpitem):
  print corpitem
  return ['corplist', 'id', int(corpitem['corporation_id'])] 
