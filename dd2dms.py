#!/usr/bin/python
""" Convert decimal degrees to degrees, minutes, seconds """
import math
import sys

if (len(sys.argv) > 1):
  dd = float(sys.argv[1])
  absDd = abs(dd)
  degs = int(absDd)
  mins = int((absDd - degs) * 60.0)
  secs = (absDd - degs - mins / 60.0) * 3600.0
  print('{0:d} {1:d} {2:.6f}\n'.format(int(math.copysign(absDd, dd)), mins, secs))
else:
  sys.stderr.write('Usage: dd2dms.py <decimalDegrees>\n')
