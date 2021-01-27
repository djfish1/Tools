#!/usr/bin/python3
""" Print hex number in decimal """
import sys
if (len(sys.argv) > 1):
  print(int(sys.argv[1], 16))
else:
  sys.stderr.write('Usage: hex2dec.py <hex>\n')
