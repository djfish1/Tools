def str2bool(s):
  b = None
  if s.lower() in ('y', 'yes', 'true', 't', '1'):
    b = True
  elif s.lower() in ('n', 'no', 'false', 'f', '0'):
    b = False
  else:
    raise ValueError('Unable to interpret "' + s + '" as bool.')
  return b

