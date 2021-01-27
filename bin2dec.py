#!/usr/bin/python3
""" Print binary number in decimal """
import sys
if (len(sys.argv) > 1):
  print(int(sys.argv[1], 2))
else:
  sys.stderr.write('Usage: bin2dec.py <bin>\n')
