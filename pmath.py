#!/usr/bin/python3
import fileinput
from math import *
import optparse
import sys

if __name__ == '__main__':
  op = optparse.OptionParser()
  op.add_option('-v', '--verbose', action='store_true', dest='verbose', help='Be verbose')
  (opts, args) = op.parse_args()
  stuff = args[0]
  answer = eval(stuff)
  if opts.verbose:
    print(stuff, '=', str(answer))
  else:
    print(str(answer))
