#!/usr/bin/python

from SmartPrint import println

import argparse
import matplotlib as mat
import matplotlib.pyplot as plt
import numpy
import sys

def makeSinglePlot(data, opts, fileName):
  println('STATUS', 'About to plot data for', fileName)
  doScatter = (opts.cCol is not None)
  if not opts.singlePlot:
    fig = plt.figure()
    fig.text(1,1, fileName, horizontalalignment='right', verticalalignment='top')
  else:
    fig = plt.figure(1)
    plt.hold(True)
  ax = fig.gca()
  if doScatter:
    sc = ax.scatter(data[:,0] / opts.xScale, data[:,1:-1] / opts.yScale, 25,
        data[:,-1] / opts.cScale, edgecolor='None')
    ax.set(axis_bgcolor='0.5')
    cb = fig.colorbar(sc)
    cb.set_label(opts.cLabel)
  else:
    line = ax.plot(data[:,0] / opts.xScale, data[:,1:] / opts.yScale,
        opts.marker, markersize=8, label=fileName)
        #opts.marker, markersize=8, markerfacecolor='None', label=fileName)
  ax.set(xlabel=opts.xLabel, ylabel=opts.yLabel, title=opts.title)

if __name__ == '__main__':
  op = argparse.ArgumentParser(description='Make a quick plot of columns of data')
  op.add_argument('-x', '--xCol', type=int, dest='xCol', help='Column with X data', default=0)
  op.add_argument('-y', '--yCol', action='append', type=int, dest='yCol', help='Column with Y data', default=[])
  op.add_argument('-c', '--cCol', type=int, dest='cCol', help='Column with color data', default=None)
  op.add_argument('-s', '--skipLines', type=int, dest='skipLines', help='Number of lines to skip reading data',
      default=0)
  op.add_argument('--xScale', type=float, dest='xScale', help='Divide X data by this for plotting', default=1)
  op.add_argument('--yScale', type=float, dest='yScale', help='Divide Y data by this for plotting', default=1)
  op.add_argument('--cScale', type=float, dest='cScale', help='Divide color data by this for plotting', default=1)
  op.add_argument('--xLabel', type=str, dest='xLabel', help='Label for x axis', default='X')
  op.add_argument('--yLabel', type=str, dest='yLabel', help='Label for y axis', default='Y')
  op.add_argument('--cLabel', type=str, dest='cLabel', help='Label for color axis', default='')
  op.add_argument('--title', type=str, dest='title', help='Figure title', default='')
  op.add_argument('--marker', type=str, dest='marker', help='Marker string', default='o')
  op.add_argument('--single', action='store_true', dest='singlePlot', help='Put all plots in single figure.')

  op.add_argument('fileNames', nargs='*')

  opts = op.parse_args()

  doScatter = opts.cCol is not None
  if doScatter and len(opts.yCol) > 1:
    println('ERROR', 'You cannot plot more than one y value with scatter')
    sys.exit(1)
  if doScatter and len(opts.fileNames) > 1 and opts.singlePlot:
    println('ERROR', 'You cannot do a scatter plot with multiple files in a single plot')
    sys.exit(1)

  for fileName in opts.fileNames:
    cols = [opts.xCol] + opts.yCol
    if opts.cCol is not None:
      cols.append(opts.cCol)
    data = numpy.loadtxt(fileName, comments=('#', '//'), skiprows=opts.skipLines, usecols=cols)
    #print(data)
    makeSinglePlot(data, opts, fileName)

  if opts.cCol is None and len(opts.fileNames) > 1 and opts.singlePlot:
    plt.legend(numpoints=1)
  plt.show()
