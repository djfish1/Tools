#!/usr/bin/python3

import optparse
import os
import subprocess

def makeHeader(f):
  f.write('\\documentclass[12pt]{article}\n')
  f.write('\\usepackage[letterpaper, left=0.in, right=0.in, top=0.in, bottom=0.in]{geometry}\n')
  #f.write('\\usepackage{geometry}\n')
  f.write('\\textwidth=8.5in\n')
  f.write('\\usepackage{graphicx}\n')
  f.write('\n')

  f.write('\\begin{document}\n')

def makeFooter(f):
  f.write('\\end{document}\n')

def writeFigureRowStart(f):
  f.write('  \\parbox{\\textwidth}{\n')
  f.write('    \\centering\n')

def writeFigureRowEnd(f):
  f.write('  }\n\n')

def writeFigure(f, fig, widthFrac, showNames):
  f.write('    \\parbox{{{0:.3f}\\textwidth}}{{\n'.format(widthFrac))
  f.write('      \\includegraphics[width={0:.3f}\\textwidth]{{{1:s}}}\n'.format(widthFrac, fig))
  if showNames:
    f.write('      {{\\tiny{0:s}}}\n'.format(fig))
  f.write('    }\n')

if __name__ == '__main__':
  p = optparse.OptionParser()
  p.add_option('-n', '--numperrow', type='int', dest='numPerRow', help='Number of pictures per row', default=1)
  p.add_option('-o', '--out', type='string', dest='outFile', help='output file name',
      default='test.pdf')
  p.add_option('-s', '--show-file-names', action='store_true', dest='showNames', help='Show file names or not')
  (opts, figs) = p.parse_args()

  widthFrac = (1.0 / (opts.numPerRow  + 1))
  texFile = os.path.splitext(opts.outFile)[0] + os.path.extsep + 'tex'
  with open(texFile, 'w') as f:
    makeHeader(f)
    for i, fig in enumerate(figs):
      if i % opts.numPerRow == 0:
        writeFigureRowStart(f)
      writeFigure(f, fig, widthFrac, opts.showNames)
      if i % opts.numPerRow == opts.numPerRow - 1 or i == len(figs) - 1:
        writeFigureRowEnd(f)
    makeFooter(f)

  subprocess.call(['pdflatex', texFile])

