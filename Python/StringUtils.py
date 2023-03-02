import re

def str2bool(s):
    b = None
    if s.lower() in ('y', 'yes', 'true', 't', '1'):
        b = True
    elif s.lower() in ('n', 'no', 'false', 'f', '0'):
        b = False
    else:
        raise ValueError('Unable to interpret "' + s + '" as bool.')
    return b

def alnum_sort(l):
    # iterables sort element by element
    # Note: parentheses in regular expression for split tell split to include
    # the tokens in the returned list.
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)    
