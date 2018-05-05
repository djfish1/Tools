import atexit
import math
import matplotlib as mat
import matplotlib.pyplot as plt
import numpy
import os
import readline
import rlcompleter
import sys

# Make 'reload' command available in Python 3
try:
  reload
except NameError:
  from importlib import reload

readline.parse_and_bind("tab: complete")
readline.parse_and_bind("C-P: history-search-backward")
readline.parse_and_bind("C-N: history-search-forward")

def modules(pattern=None):
  import re
  mods = sys.modules
  keys = list(mods.keys())
  keys.sort()
  if pattern is not None:
    pattern = '.*' + pattern + '.*'
  for key in keys:
    if pattern is None or re.match(pattern, key) is not None:
      print(key)

historyPath = os.path.expanduser("~/.pyhistory")

def saveHistory(historyPath=historyPath):
  import readline
  readline.write_history_file(historyPath)

if os.path.exists(historyPath):
    readline.read_history_file(historyPath)

atexit.register(saveHistory)

mat.interactive(True)
del atexit, historyPath, readline, rlcompleter, saveHistory
