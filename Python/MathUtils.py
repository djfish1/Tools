import numpy

def magnitude(vec):
  return numpy.sqrt(sum((x*x for x in numpy.squeeze(vec).flat)))
  #mag = numpy.nan
  #nDim = len(numpy.shape(vec))
  #if nDim == 0:
  #  mag = vec
  #elif nDim in (1, 2):
  #  if nDim == 1 or numpy.shape(vec)[0] == 1:
  #    mag = float(numpy.sqrt(numpy.dot(vec, vec.T)))
  #  elif numpy.shape(vec)[1] == 1:
  #    mag = float(numpy.sqrt(numpy.dot(vec.T, vec)))
  #  else:
  #    raise ValueError('Expected a vector, got: ' + repr(vec) + ' with shape: ' + str(numpy.shape(vec)))
  #else:
  #  raise ValueError('Expected a vector, got: ' + repr(vec) + ' with shape: ' + str(numpy.shape(vec)))
  #return mag

class Conic(object):
  """ Based on code from Perluigi Taddei: https://bitbucket.org/pierluigi/conicsintersection.git """
  def __init__(self, d):
    """ For conic equation of the form: A x^2 + B y^2 + 2C xy + 2Dx + 2Ey + F = 0
        the matrix should be represented as: [[A, C, D], [C, B, E], [D, E, F]] """
    self.data = numpy.matrix(d).reshape((3,3))

  def adjointSym3(self):
    a = self.data[0, 0]
    b = self.data[0, 1]
    d = self.data[0, 2]
    c = self.data[1, 1]
    e = self.data[1, 2]
    f = self.data[2, 2]

    A = numpy.matrix([[c * f - e * e, -b * f + e * d, b * e - c * d],
                        [-b * f + e * d, a * f - d * d, -a * e + b * d],
                        [b * e - c * d, -a * e + b * d, a * c - b * b]])
    return Conic(A)
    
  def _crossMatrix(self, p):
    cm = numpy.zeros((3, 3), float)
    p = numpy.array(p).squeeze()
    #print(p)
    #print(p[2])
    cm[0, 1] = p[2]
    cm[0, 2] = -p[1]
    cm[1, 0] = -p[2]
    cm[1, 2] = p[0]
    cm[2, 0] = p[1]
    cm[2, 1] = -p[0]
    return cm

  def decomposeDegenerate(self):
    if self.rank() == 1:
      conic = self
    else:
      B = self.adjointSym3()
      i = numpy.argmax(numpy.abs(numpy.diag(B.data)))
      if B.data[i, i] < 0:
        return None, None
      b = numpy.sqrt(B.data[i, i])
      p = B.data[:, i] / b

      mp = self._crossMatrix(p)
      conic = Conic(self.data + mp)
    # Get the lines
    ci = numpy.argmax(numpy.abs(conic.data))
    j = int(numpy.floor((ci - 1) / 3))
    i = ci - j * 3
    #print(i, j)
    line0 = conic.data[i, :]
    line1 = conic.data[:, j]
    return line0, line1

  def _getPointsOnLine(self, line):
    line = numpy.array(line).squeeze()
    #print(line)
    if line[0] == 0 and line[1] == 0:
      p0 = [1, 0, 0]
      p1 = [0, 1, 0]
    else:
      p1 = [-line[1], line[0], 0]
      if numpy.abs(line[0]) < numpy.abs(line[1]):
        p0 = [0, -line[2], line[1]]
      else:
        p0 = [-line[2], 0, line[0]]
    return (numpy.matrix(p0).T, numpy.matrix(p1).T)

  def intersectWithLine(self, line):
    [point0, point1] = self._getPointsOnLine(line)
    p0Cp0 = point0.T * self.data * point0
    p1Cp1 = point1.T * self.data * point1
    p0Cp1 = point0.T * self.data * point1
    if p1Cp1 == 0:
      k1 = -0.5 * p0Cp0 / p0Cp1
      P = point0 + k1 * point2
    else:
      delta = p0Cp1 * p0Cp1 - p0Cp0 * p1Cp1
      if delta >= 0:
        s = numpy.sqrt(delta)
        k0 = complex((-p0Cp1 + s) / p1Cp1)
        k1 = complex((-p0Cp1 - s) / p1Cp1)
        #print('p0:', point0, 'p1:', point1, 'k0:', k0, 'k1:', k1)
        P = numpy.concatenate((point0 + k0 * point1, point0 + k1 * point1), axis=1)

    return P

  def rank(self):
    return numpy.linalg.matrix_rank(self.data)

  def _completeIntersections(self, conic1):
    CC = self.data * (-conic1.data.getI())
    tmp = numpy.matrix([CC[0,0], CC[0, 2], CC[2,0], CC[2, 2]]).reshape((2,2))
    poly = numpy.poly1d([-1, numpy.trace(CC),
                         -(numpy.linalg.det(CC[0:2, 0:2]) + numpy.linalg.det(CC[1:, 1:]) + numpy.linalg.det(tmp)),
                         numpy.linalg.det(CC)])
    #print(poly)
    roots = poly.r
    #print(roots)
    m = []
    if roots[0].imag == 0.0:
      conic = Conic(self.data + roots[0] * conic1.data)
      line0, line1 = conic.decomposeDegenerate()
    if line0 is None and roots[1].imag == 0:
      conic = Conic(self.data + roots[1] * conic1.data)
      line0, line1 = conic.decomposeDegenerate()
    if line0 is None and roots[2].imag == 0:
      conic = Conic(self.data + roots[2] * conic1.data)
      line0, line1 = conic.decomposeDegenerate()
  
    if line0 is None:
      #print('Returning empty form _completeIntersections')
      return numpy.matrix([[]])
    else:
      P0 = self.intersectWithLine(line0)
      P1 = self.intersectWithLine(line1)
      #print('Returning from _completeIntersections')
      return numpy.concatenate((P0, P1), axis=1)
  
  def intersectConic(self, conic1):
    r0 = self.rank()
    r1 = conic1.rank()
  
    if r1 == 3 and r0 == 3:
      retPoints = self._completeIntersections(conic1)
    else:
      if r1 < 3:
        defE = conic1
        fullE = self
      else:
        defE = self
        fullE = conic1
  
      line0, line1 = defE.decompose()
      P0 = fullE.intersectWithLine(line0)
      P1 = fullE.intersectWithLine(line1)
  
      #print('Returning from intersectConic')
      retPoints = numpy.concatenate((P0, P1), axis=1)
  
    if numpy.all(numpy.isreal(retPoints)):
      return retPoints.astype(float)
    else:
      print('I somehow got imaginary intersection points. Oops.')
      return numpy.matrix([[]])
