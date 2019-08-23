import numpy

def magnitude(vec):
  mag = numpy.nan
  nDim = len(numpy.shape(vec))
  if nDim == 0:
    mag = vec
  elif nDim in (1, 2):
    if nDim == 1 or numpy.shape(vec)[0] == 1:
      mag = float(numpy.sqrt(numpy.dot(vec, vec.T)))
    elif numpy.shape(vec)[1] == 1:
      mag = float(numpy.sqrt(numpy.dot(vec.T, vec)))
    else:
      raise ValueError('Expected a vector, got: ' + repr(vec) + ' with shape: ' + str(numpy.shape(vec)))
  else:
    raise ValueError('Expected a vector, got: ' + repr(vec) + ' with shape: ' + str(numpy.shape(vec)))
  return mag
