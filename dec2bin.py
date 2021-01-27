#!/usr/bin/python3
""" Print decimal number in binary """
import sys
if (len(sys.argv) > 1):
  print('{0:b}'.format(int(sys.argv[1])))
else:
  sys.stderr.write('Usage: dec2bin.py <dec>\n')
