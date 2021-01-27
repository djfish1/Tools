#!/usr/bin/python3
""" Convert degrees/minutes/seconds to decimal degrees """
import math
import sys
if (len(sys.argv) > 3):
  degs = float(sys.argv[1])
  mins = float(sys.argv[2])
  secs = float(sys.argv[3])
  absDegs = abs(degs)
  absDecDeg = absDegs + mins / 60.0 + secs / 3600.0
  print('{0:.6f}\n'.format(math.copysign(absDecDeg, degs)))
else:
  sys.stderr.write('Usage: dms2dd.py <degrees> <minutes> <seconds>\n')
