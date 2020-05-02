from __future__ import print_function
import os
import sys

def loadColorMapFile(fileName):
  colors = {}
  with open(fileName, 'r') as f:
    while True:
      line = f.readline()
      if line == '':
        break
      #print(line)
      split = line.strip().split()
      #print(split)
      red = float(split[0])
      green = float(split[1])
      blue = float(split[2])
      colorName = ' '.join(split[3:])
      color = (red, green, blue)
      colors[colorName] = color
      # Store in all lowercase, space removed format as well
      colors[colorName.lower().replace(' ', '')] = color
  return colors

rgbFile = os.path.join(os.path.split(__file__)[0], 'rgb.txt')
allColors = loadColorMapFile(rgbFile)

def getColorFromHexRGB(hex, normalized=True):
  if hex.startswith('#'):
    hex = hex[1:]
  elif hex.lower.startswith('0x'):
    hex = hex[2:]
  red = int(hex[0:2], 16)
  green = int(hex[2:4], 16)
  blue = int(hex[4:6], 16)
  color = (float(red), float(green), float(blue))
  if normalized:
    color = tuple([x/255.0 for x in color])
  return color

def getColor(name, normalized=True):
  global allColors
  if name.startswith('#') or name.lower().startswith('0x'):
    rgb = getColorFromHexRGB(name, normalized)
  else:
    lowerSpaceRemoved = name.lower().replace(' ', '')
    rgb = allColors.get(name) or allColors.get(lowerSpaceRemoved)
    if rgb is None:
      print('Unknown color:', name, file=sys.stderr)
    elif normalized:
      rgb = tuple([x/255.0 for x in rgb])
  return rgb

if __name__ == '__main__':
  name = sys.argv[1]
  print(getColor(name, normalized=True))
