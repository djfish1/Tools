#!/usr/bin/python3
import datetime
import sys
import time

import TimeUtils
import SmartPrint

if len(sys.argv) < 2:
  t = time.time()
else:
  t = float(sys.argv[1])
print(TimeUtils.niceFromEpoch(t))
