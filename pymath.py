#!/usr/bin/env python3
import math
import sys

import MathUtils

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('USAGE: pymath.py <expression>')
    expression = sys.argv[1]
    x = 5
    answer = eval(expression, {'abs':abs, '__builtins__':None, 'math':math, 'MathUtils':MathUtils})
    print(expression, '=', answer)
