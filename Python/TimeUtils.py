""" Module for utility time function. """
import datetime
import time

def niceFromEpoch(timeToPrint=None, showMicros=True):
  """ Get a nicely formatted string representing the time.
        If timeToPrint is None, then use time.time()
        showMicros determines whether or not written to microsecond precision """
  if timeToPrint is None:
    timeToPrint = time.time()
  dateTime = datetime.datetime.utcfromtimestamp(timeToPrint)
  retStr = '-'.join(('{0:04d}'.format(dateTime.year), '{0:02d}'.format(dateTime.month), \
      '{0:02d}'.format(dateTime.day))) + '_' + '-'.join(('{0:02d}'.format(dateTime.hour), \
      '{0:02d}'.format(dateTime.minute), '{0:02d}'.format(dateTime.second)))
  if showMicros:
    retStr += '.{0:06d}'.format(dateTime.microsecond)

  return retStr

def epochFromNice(timeToConvert=None):
  """ Get the epoch time from the passed in string of the format:
        YYYY-mm-dd_HH-MM-SS.UUUUUU
        returns time.time() if timeToConvert is not specified """
  if timeToConvert is None:
    retTime = time.time()
  else:
    yearMonthDay, hourMinuteSec = timeToConvert.split('_')
    (year, month, day) = (int(x) for x in yearMonthDay.split('-'))
    hmsSplit = hourMinuteSec.split('.')
    if len(hmsSplit) > 1:
      microseconds = int(hmsSplit[1])
    else:
      microseconds = 0
    (hour, minute, sec) = (int(x) for x in hmsSplit[0].split('-'))
    dateTime = datetime.datetime(year, month, day, hour, minute, sec, microseconds)
    retTime = time.mktime(dateTime.timetuple()) + microseconds / 1.0E6
    #strpTime = time.strptime(timeToConvert, '%Y-%m-%d_%H-%M-%S')
    #retTime = time.mktime(strpTime)

  return retTime
