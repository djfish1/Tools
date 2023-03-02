#!/usr/bin/python3
import sys
import time

import TimeUtils

"""
Convert a time of the format YYYY-MM-DD_HH-MM-SS.ssssss to seconds from epoch.
Use the current time if the user does not specify a time."""
if len(sys.argv) < 2:
    t = time.time()
else:
    t = TimeUtils.epochFromNice(sys.argv[1])
print('{0:.6f}'.format(t))
