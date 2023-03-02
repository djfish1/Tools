import atexit
import math
import matplotlib as mat
# Gtk3Agg and GTK3Cairo do not work interactively in vanilla python.
# It does work in ipython.
#mat.use('TkAgg')
#mat.use('Gtk4Agg')
import matplotlib.pyplot as plt
import numpy
import os
readline = None
try:
    import readline
except ImportError:
    print('readline module not available')
    try:
        import pyreadline
        readline = pyreadline.Readline()
    except ImportError:
        print('pyreadline not available')
import rlcompleter
import sys

# Make 'reload' command available in Python 3
try:
    reload
except NameError:
    from importlib import reload

if readline:
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("CTRL-P: history-search-backward")
    readline.parse_and_bind("CTRL-N: history-search-forward")

def modules(pattern=None):
    import re
    mods = sys.modules
    keys = list(mods.keys())
    keys.sort()
    if pattern is not None:
        pattern = '.*' + pattern + '.*'
    for key in keys:
        if pattern is None or re.match(pattern, key) is not None:
            print(key)

historyPath = os.path.join(os.path.expanduser("~"), ".pyhistory")

if readline:
    def saveHistory(historyPath=historyPath):
        import readline
        for i in range(readline.get_current_history_length(), 1, -1):
            if readline.get_history_item(i).upper() == 'Y':
                readline.remove_history_item(i - 1)
        readline.write_history_file(historyPath)

    if os.path.exists(historyPath):
        try:
            readline.read_history_file(historyPath)
        except BaseException as e:
            print('Unable to load history.')

    atexit.register(saveHistory)
else:
    saveHistory = None

mat.interactive(True)

def _makeTestPlot(marker='o-', showLegend=True):
    import PlotUtils
    f = PlotUtils.makeFigure()
    ax = f.add_subplot(111)
    x = numpy.arange(0, 2*numpy.pi, 0.2)
    for i in range(16):
        y = numpy.sin(x + i * 0.1)
        ax.plot(x, y, marker, label='v{0:d}'.format(i))
    ax.set(xlabel='Time', ylabel='Voltage', title='Demo Plot')
    if showLegend:
        ax.legend()
    return f, ax

del atexit, historyPath, readline, rlcompleter, saveHistory
