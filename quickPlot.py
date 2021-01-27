#!/usr/bin/python3

import argparse
import collections
import fileinput
import matplotlib as mat
import matplotlib.pyplot as plt
import numpy
import sys

from SmartPrint import println

def getFigAndAxes(topRightLabel=None):
  fig = plt.figure()
  if topRightLabel is not None:
    fig.text(1,1, topRightLabel, horizontalalignment='right', verticalalignment='top')
  ax = plt.gca()
  return (fig, ax)

def makeHistograms(data, opts):
  if opts.singlePlot:
    fig, ax = getFigAndAxes()
    ax.hist(data.values(), label=data.keys())
    ax.set(xlabel=opts.xLabel, ylabel='Count', title=opts.title)
  else:
    for iFile, fileName in enumerate(data.keys()):
      println('STATUS', 'About to plot data for', fileName)
      fig, ax = getFigAndAxes(fileName)
      ax.hist(data[fileName])
      ax.set(xlabel=opts.xLabel, ylabel='Count', title=opts.title)
  if opts.singlePlot:
    plt.legend()

def makePlots(data, opts):
  if len(opts.yCol) == 0:
    makeHistograms(data, opts)
    return
  doScatter = (opts.cCol is not None)
  if opts.singlePlot:
    fig, ax = getFigAndAxes()
  for iFile, fileName in enumerate(data.keys()):
    println('STATUS', 'About to plot data for', fileName)
    if not opts.singlePlot:
      fig, ax = getFigAndAxes(fileName)
    if opts.bw or doScatter:
      ax.set(facecolor=[0.5, 0.5, 0.5])
    if doScatter:
      sc = ax.scatter(data[fileName][:,0] / opts.xScale, data[fileName][:,1:-1] / opts.yScale, 25,
          data[fileName][:,-1] / opts.cScale, edgecolor='None')
      cb = fig.colorbar(sc)
      cb.set_label(opts.cLabel)
    else:
      ms = 8
      if opts.bw:
        if iFile == 0:
          ms = 5
        else:
          ms = 3
      for icol, yCol in enumerate(range(1,data[fileName].shape[1])):
        line = ax.plot(data[fileName][:,0] / opts.xScale, data[fileName][:,yCol] / opts.yScale,
            opts.marker, markersize=ms, markeredgecolor='None', label=fileName + ':' + str(opts.yLabel[icol]))
    ax.set(xlabel=opts.xLabel, ylabel=opts.yLabel, title=opts.title)
    if not doScatter and (len(opts.yCol) > 1 and not opts.singlePlot):
      plt.legend(numpoints=1)
  if not doScatter and (len(opts.yCol) > 1 or (len(opts.fileNames) > 1 and opts.singlePlot)):
    plt.legend(numpoints=1)

def verifyAndFixOptions(opts):
  doScatter = opts.cCol is not None
  if doScatter and len(opts.yCol) > 1:
    println('ERROR', 'You cannot plot more than one y value with scatter')
    sys.exit(1)
  if opts.bw and len(opts.yCol) > 1:
    println('ERROR', 'You cannot plot more than one y value with bw')
    sys.exit(1)
  if opts.bw and len(opts.fileNames) < 2:
    println('ERROR', 'You cannot plot bw comparison with less than 2 files')
    sys.exit(1)
  if doScatter and len(opts.fileNames) > 1 and opts.singlePlot:
    println('ERROR', 'You cannot do a scatter plot with multiple files in a single plot')
    sys.exit(1)
  for iyc, yc in enumerate(opts.yCol):
    if iyc >= len(opts.yLabel):
      opts.yLabel.append('col' + str(yc))
  #println('DEBUG', 'yLabels:', opts.yLabel)
  return opts


if __name__ == '__main__':
  ap = argparse.ArgumentParser(description='Make a quick plot of columns of data')
  ap.add_argument('-x', '--xCol', type=int, dest='xCol', help='Column with X data', default=0)
  ap.add_argument('-y', '--yCol', action='append', type=int, dest='yCol', help='Column with Y data', default=[])
  ap.add_argument('-c', '--cCol', type=int, dest='cCol', help='Column with color data', default=None)
  ap.add_argument('-s', '--skipLines', type=int, dest='skipLines', help='Number of lines to skip reading data',
      default=0)
  ap.add_argument('--xScale', type=float, dest='xScale', help='Divide X data by this for plotting', default=1)
  ap.add_argument('--yScale', type=float, dest='yScale', help='Divide Y data by this for plotting', default=1)
  ap.add_argument('--cScale', type=float, dest='cScale', help='Divide color data by this for plotting', default=1)
  ap.add_argument('--xLabel', type=str, dest='xLabel', help='Label for x axis', default='X')
  ap.add_argument('--yLabel', action='append', type=str, dest='yLabel', help='Label for y axis', default=[])
  ap.add_argument('--cLabel', type=str, dest='cLabel', help='Label for color axis', default='')
  ap.add_argument('--title', type=str, dest='title', help='Figure title', default='')
  ap.add_argument('--marker', type=str, dest='marker', help='Marker string', default='o')
  ap.add_argument('--single', action='store_true', dest='singlePlot', help='Put all plots in single figure.')
  ap.add_argument('--bw', action='store_true', dest='bw', help='Clear comparison to base.', default=False)

  ap.add_argument('fileNames', nargs='*')

  opts = ap.parse_args()

  if opts.bw:
    opts.singlePlot = True
    mat.rcParams['axes.prop_cycle'] = mat.cycler('markerfacecolor',
        ['w', 'k', [0.0, 0.0, 0.9], [0.0, 0.7, 0.0],
        [0.8, 0.0, 0.0], [0.8, 0.0, 0.8], [0.0, 0.8, 0.8]])
  if len(opts.yCol) == 0:
    mat.rcParams['axes.prop_cycle'] = mat.cycler('color',
        [[0.0, 0.0, 0.9], [0.0, 0.7, 0.0],
        [0.8, 0.0, 0.0], [0.8, 0.0, 0.8], [0.0, 0.8, 0.8]])

  opts = verifyAndFixOptions(opts)

  data = collections.OrderedDict()
  if len(opts.fileNames) > 0:
    for iFile, fileName in enumerate(opts.fileNames):
      cols = [opts.xCol] + opts.yCol
      if opts.cCol is not None:
        cols.append(opts.cCol)
      data[fileName] = numpy.loadtxt(fileName, comments=('#', '//'), skiprows=opts.skipLines, usecols=cols)
  else:
    data['stdin'] = []
    rows = 0
    del(sys.argv[1:])
    for iline, line in enumerate(fileinput.input()):
      if iline < opts.skipLines:
        continue
      if line.startswith('#') or line.startswith('//'):
        continue
      rows += 1
      lineData = numpy.array(line.strip().split(), float)
      ddata = [lineData[opts.xCol]]
      for yC in opts.yCol:
        ddata = ddata + [lineData[yC]]
      if opts.cCol is not None:
        ddata = ddata + [lineData[opts.cCol]]
      data['stdin'] = data['stdin'] + ddata
    data['stdin'] = numpy.array(data['stdin']).reshape((rows, -1))
    #print(data['stdin'])

  makePlots(data, opts)
  plt.show()
