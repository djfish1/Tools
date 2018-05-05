#!/usr/bin/python
import sys
import time

import TimeUtils

if len(sys.argv) < 2:
  t = time.time()
else:
  t = TimeUtils.epochFromNice(sys.argv[1])
print('{0:.6f}'.format(t))
