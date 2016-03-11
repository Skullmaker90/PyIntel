import os
from datetime import datetime

class Log(object):
  def __init__(self, name):
    self.name = name
    self.path = '/programming/Python/PyIntel/logs/%s.log' % (self.name)

  def warning(self, *args):
    self.log('[Warning]', args)

  def debug(self, *args):
    self.log('[Debug]', args)

  def info(self, *args):
    self.log('[Info]', args)

  def critical(self, *args):
    self.log('[Critical]', args)

  def log(self, level, args):
    try:
      with open(self.path, 'a') as f:
        for arg in args:
          _str = datetime.today().strftime('%m.%d.%y %H:%M:%S') + ' ' + level +' :: ' + str(arg) + '\n'
          f.write(_str)
    except IOError:
      os.system('touch %s' % (self.path))
      self.log(level, args)
