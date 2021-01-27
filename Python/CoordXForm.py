""" Earth coordinate transformations of various types.
    All angles are in radians, and all linear units are in meters. """

import numpy

YAW_TYPE = 1
PITCH_TYPE = 2
ROLL_TYPE = 3
IDX_LAT = IDX_X = IDX_U = 0
IDX_LON = IDX_Y = IDX_V = 1
IDX_ALT = IDX_Z = IDX_W = 2

EARTH_MODEL = {'alpha':6378137.0, 'flattening':(1.0/298.257223563)}

# Convergence criteria of 1.0E-7 gives about 0.5m accuracy, where 1.0E-12
# gives double precision accuracy so coordinate transformations can be
# reversed exactly. The latter obviously runs a little bit slower.
CONVERGENCE_CRITERIA = 1.0E-12

def getDirCosTransform(angle, rotationType):
  """ Get the rotation matrix for the given angle (radians) and rotation type."""
  cosA = numpy.cos(angle)
  sinA = numpy.sin(angle)
  xformMatrix = numpy.zeros((3, 3))

  if rotationType == YAW_TYPE:
    xformMatrix[0, 0] = cosA
    xformMatrix[1, 1] = cosA
    xformMatrix[0, 1] = sinA
    xformMatrix[1, 0] = -sinA
    xformMatrix[2, 2] = 1.0
  elif rotationType == PITCH_TYPE:
    # Check the 0,2 and 2,0 entries, as they seem reversed in sign from what I expect
    xformMatrix[0, 0] = cosA
    xformMatrix[2, 2] = cosA
    xformMatrix[0, 2] = -sinA
    xformMatrix[2, 0] = sinA
    xformMatrix[1, 1] = 1.0
  elif rotationType == ROLL_TYPE:
    xformMatrix[0, 0] = 1.0
    xformMatrix[1, 1] = cosA
    xformMatrix[2, 2] = cosA
    xformMatrix[1, 2] = sinA
    xformMatrix[2, 1] = -sinA
  else:
    raise(ValueError("Invalid rotation type: " + str(rotationType) + ". "
                     + "Valid values are 1-3 or YAW_TYPE, PITCH_TYPE, and ROLL_TYPE"))

  return numpy.matrix(xformMatrix)

def llh2ecf(llh):
  """ Transform lat/lon/height to earth-centered fixed.
  Validated with MATLAB """
  # Example: c.llh2ecf((0.5, 0.5, 0))
  # matrix([[ 4915913.06680899],
  #         [ 2685575.54825337],
  #         [ 3039710.90685183]])
  llh = numpy.matrix(numpy.reshape(llh, (3, 1)))
  alpha = EARTH_MODEL['alpha']
  flattening = EARTH_MODEL['flattening']
  sinLat = numpy.sin(llh[IDX_LAT])
  nFactor = alpha / numpy.sqrt(1.0 - (2 - flattening) * flattening * sinLat * sinLat)
  fac = (nFactor + llh[IDX_ALT]) * numpy.cos(llh[IDX_LAT])

  cosLon = numpy.cos(llh[IDX_LON])
  sinLon = numpy.sin(llh[IDX_LON])
  ecf = numpy.reshape((fac * cosLon,
                       fac * sinLon,
                       ((1 - flattening)*(1 - flattening)*nFactor + llh[IDX_ALT])*sinLat),
                      (3, 1))
  return numpy.matrix(ecf)

def ecf2llh(ecf):
  """ Transform earth-centered fixed to LLH
  Verified with: http://www.oc.nps.edu/oc2902w/coord/llhxyz.htm """
  ecf = numpy.matrix(numpy.reshape(ecf, (3, 1)))
  origin = numpy.zeros((3, 1))
  uvw = ecf2uvw(ecf, origin)
  llh = uvw2llh(uvw, origin)
  return llh

def ecf2uvw(ecf, origin):
  """ Transform earth-centered fixed to UVW
  Validated with MATLAB """
  ecf = numpy.matrix(numpy.reshape(ecf, (3, 1)))
  origin = numpy.matrix(numpy.reshape(origin, (3, 1)))
  xformMatrix = getDirCosTransform(origin[IDX_LON], YAW_TYPE)
  uvw = xformMatrix * ecf
  return uvw

def tcs2uvw(tcs, origin):
  """ Transform topocentric coordinate system (ENU) to UVW.
   Validated with MATLAB """
  tcs = numpy.matrix(numpy.reshape(tcs, (3, 1)))
  origin = numpy.matrix(numpy.reshape(origin, (3, 1)))
  originEcf = llh2ecf(origin)
  originUvw = ecf2uvw(originEcf, origin)

  xformMatrix = DC_PITCH_ROLL_PI_OVER_TWO_INV * getDirCosTransform(origin[IDX_LAT], ROLL_TYPE)

  uvw = (xformMatrix * tcs) + originUvw

  return uvw

def uvw2tcs(uvw, origin):
  """ Transform UVW coordinate to topocentric coordinate system (ENU)
  Validated with MATLAB """
  uvw = numpy.matrix(numpy.reshape(uvw, (3, 1)))
  origin = numpy.matrix(numpy.reshape(origin, (3, 1)))

  originEcf = llh2ecf(origin)
  originUvw = ecf2uvw(originEcf, origin)

  xformMatrix = getDirCosTransform(-origin[IDX_LAT], ROLL_TYPE) * DC_PITCH_ROLL_PI_OVER_TWO

  tcs = xformMatrix * (uvw - originUvw)

  return tcs

def uvw2llh(uvw, origin):
  """ Transform UVW coordinate to lat/lon/height
  Validated with MATLAB """
  uvw = numpy.matrix(numpy.reshape(uvw, (3, 1)))
  origin = numpy.matrix(numpy.reshape(origin, (3, 1)))
  alpha = EARTH_MODEL['alpha']
  flattening = EARTH_MODEL['flattening']
  eccSq = (2.0 - flattening) * flattening
  llh = numpy.matrix(numpy.zeros((3, 1)))

  sinLat = numpy.sin(origin[IDX_LAT])
  cosLat = numpy.cos(origin[IDX_LAT])
  denom = 1.0 - eccSq * sinLat * sinLat
  nFactor = alpha / numpy.sqrt(denom)

  esqNsin = eccSq * nFactor * sinLat

  dNdLat = esqNsin * cosLat / denom

  tmp1 = numpy.sqrt(uvw[IDX_U] * uvw[IDX_U] + uvw[IDX_V] * uvw[IDX_V])
  # Handle the North and South Pole
  if tmp1 == 0.0:
    llh[IDX_LON] = origin[IDX_LON]
    if uvw[IDX_W] > 0.0:
      llh[IDX_ALT] = uvw[IDX_W] - (alpha / numpy.sqrt(1.0 - eccSq))
      llh[IDX_LAT] = numpy.pi * 0.5
    else:
      llh[IDX_ALT] = -uvw[IDX_W] - (alpha / numpy.sqrt(1.0 - eccSq))
      llh[IDX_LAT] = -numpy.pi * 0.5
  else:
    llh[IDX_LON] = origin[IDX_LON] + numpy.arctan2(uvw[IDX_V], uvw[IDX_U])
    lat = numpy.arctan2(uvw[IDX_W] + esqNsin, tmp1)
    earthRad = nFactor + dNdLat * (lat - origin[IDX_LAT])
    dSinLat = 1.0
    sinLat = numpy.sin(lat)
    while dSinLat > CONVERGENCE_CRITERIA:
      oSinLatSav = sinLat
      tmp2 = uvw[IDX_W] + eccSq * earthRad * sinLat
      sinLat = tmp2 / numpy.sqrt(tmp1 * tmp1 + tmp2 * tmp2)
      earthRad = alpha / numpy.sqrt(1.0 - eccSq * sinLat * sinLat)
      dSinLat = numpy.abs(sinLat - oSinLatSav)
    lat = numpy.arcsin(sinLat)

    llh[IDX_ALT] = tmp1 / numpy.cos(lat) - earthRad
    llh[IDX_LAT] = lat

  return llh

def tcs2llh(tcs, origin):
  """ Transform TCS (ENU) coordinate to lat/lon/height
  Validated with MATLAB """
  tcs = numpy.matrix(numpy.reshape(tcs, (3, 1)))
  origin = numpy.matrix(numpy.reshape(origin, (3, 1)))

  uvw = tcs2uvw(tcs, origin)
  llh = uvw2llh(uvw, origin)

  return llh

def llh2tcs(llh, origin):
  """ Transform lat/lon/height to TCS (ENU)
  Validated with MATLAB """
  #Example: c.llh2tcs((0.5, 0.5, 1000), (-0.2, 0.1, 0.))
  #  matrix([[ 2181728.20602909],
  #          [ 3996462.08584669],
  #          [-1923876.31741103]])
  llh = numpy.matrix(numpy.reshape(llh, (3, 1)))
  origin = numpy.matrix(numpy.reshape(origin, (3, 1)))

  ecf = llh2ecf(llh)
  uvw = ecf2uvw(ecf, origin)
  tcs = uvw2tcs(uvw, origin)

  return tcs

def ll2utm(lat, lon):
  """ Convert WGS84 lat/lon to UTM easting and northing, and the corresponding UTM zone
      Verified against: http://home.hiwaay.net/~taylorc/toolbox/geography/geoutm.html """
  alpha = EARTH_MODEL['alpha']
  flattening = EARTH_MODEL['flattening']
  eccSq = (2.0 - flattening) * flattening

  refLon = numpy.radians(numpy.floor(numpy.degrees(lon) / 6.0) * 6.0 + 3.0)
  k0 = 0.9996

  falseEasting = 5.0E5
  falseNorthing = 1.0E7 if lat < 0.0 else 0.0

  eps = eccSq / (1.0 - eccSq)

  sinLat = numpy.sin(lat)
  sin2Lat = numpy.sin(2.0 * lat)
  sin4Lat = numpy.sin(4.0 * lat)
  sin6Lat = numpy.sin(6.0 * lat)
  denom = 1.0 - eccSq * sinLat * sinLat
  # nFactor is radius of curvature of the earth perpendicular to meridian plane
  # and the distance from  point to the polar axis
  nFactor = alpha / numpy.sqrt(denom)
  tanLatSq = numpy.tan(lat) ** 2
  cosLat = numpy.cos(lat)
  cosTerm = eps * (cosLat ** 2)
  aTerm = (lon - refLon) * cosLat

  # True distance along the central meridian from the equator to lat
  ecc4 = eccSq * eccSq
  ecc6 = ecc4 * eccSq
  mDist = alpha * \
      ((1.0 - eccSq * 0.25 - 3.0 * ecc4 / 64.0 - 5.0 * ecc6 / 256.0) * lat \
       - (3.0 * eccSq / 8.0 + 3.0 * ecc4 / 32.0 + 45.0 * ecc6 / 1024.0) * sin2Lat \
       + (15.0 * ecc4 / 256.0 + 45.0 * ecc6 / 1024.0) * sin4Lat \
       - (35.0 * ecc6 / 3072.0) * sin6Lat)

  a2 = aTerm * aTerm
  a3 = a2 * aTerm
  a4 = a2 * a2
  a5 = a4 * aTerm
  a6 = a3 * a3
  easting = falseEasting + k0 * nFactor \
      * (aTerm + (1.0 - tanLatSq + cosTerm) * a3 / 6.0 \
         + (5.0 - 18.0 * tanLatSq + tanLatSq * tanLatSq + 72.0 * cosTerm - 58.0 * eps) * a5 / 120.0)

  northing = falseNorthing + k0 * mDist + k0 * nFactor * sinLat / cosLat \
      * (a2 / 2.0 + (5.0 - tanLatSq + 9.0 * cosTerm + 4.0 * cosTerm * cosTerm) * a4 / 24.0 \
      + (61.0 - 58.0 * tanLatSq + tanLatSq * tanLatSq + 600.0 * cosTerm - 330.0 * eps) * a6 / 720.0)

  zone = int(numpy.floor(numpy.degrees(refLon) / 6) + 31)

  return {'easting':easting, 'northing':northing, 'zone':zone}

DC_PITCH_PI_OVER_TWO = getDirCosTransform(0.5*numpy.pi, PITCH_TYPE)
DC_ROLL_PI_OVER_TWO = getDirCosTransform(0.5*numpy.pi, ROLL_TYPE)
DC_PITCH_ROLL_PI_OVER_TWO = DC_PITCH_PI_OVER_TWO * DC_ROLL_PI_OVER_TWO
DC_PITCH_ROLL_PI_OVER_TWO_INV = DC_PITCH_ROLL_PI_OVER_TWO.getI()
#if __name__ == '__main__':
#  import sys
#  print("Evaluating: " + sys.argv[1])
#  print("Result: " + str(eval(sys.argv[1]).getT()))
