""" Module for printing out log information in a consistent and useful way. """
import inspect
import sys

import TimeUtils

def println(status, *args):
  """ Print a log message with time and stack information """
  timeStr = TimeUtils.niceFromEpoch(showMicros=True)
  strOut = status + ':' + timeStr + ' | ' + ' '.join((str(arg) for arg in args))
  if sys.version_info.major == 3:
    stk = inspect.stack()[1]
    strOut += ' | ' + stk.filename + ':' + stk.function + ':' + str(stk.lineno)
  sys.stdout.write(strOut + '\n')

