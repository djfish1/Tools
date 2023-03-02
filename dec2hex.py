#!/usr/bin/python3
""" Print decimal number in hexadecimal """
import sys
if (len(sys.argv) > 1):
    print('{0:x}'.format(int(sys.argv[1])))
else:
    sys.stderr.write('Usage: dec2hex.py <dec>\n')
