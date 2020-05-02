from __future__ import print_function
useGtk = True
try:
  import gtk
except ImportError as e:
  useGtk = False
import matplotlib as mat
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg
import os
import sys

def makeFigure():
  fig = plt.figure()
  _addCustomToolbar(fig)
  return fig

def _changeAxis(entry, fig):
  #print('Changing axes')
  axisToChange = None
  lims = None
  text = entry.get_text()
  if text.startswith('plt.'):
    try:
      eval(text, {'plt':plt})
    except BaseException as e:
      print("Unable to eval:", text, e, file=sys.stderr)
  else:
    try:
      if text.count(':') == 1 and text.count(',') == 1:
        split = text.split(':')
        axisToChange = split[0].lower()
        lims = [float(x) for x in split[1].split(',')]
      elif text.count(',') == 3:
        lims = [float(x) for x in text.split(',')]
      for ax in fig.axes:
        # Skip colorbar axis and other non-navigatable axes
        if not ax.get_navigate():
          continue
        if lims is not None:
          if axisToChange == 'x':
            print('Setting xlimits:', lims)
            ax.set_xlim(lims)
          elif axisToChange == 'y':
            print('Setting ylimits:', lims)
            ax.set_ylim(lims)
          else:
            print('Setting axis:', lims)
            ax.axis(lims)
        else:
          print('Setting axis:', text)
          ax.axis(text)
    except BaseException as e:
      print("Unable to set axes:", text, file=sys.stderr)
  fig.canvas.draw()
  entry.grab_focus()

def _copyToClipboard(but, fig):
  #print('CLIP!')
  tmpFile = os.tempnam() + '.jpg'
  fig.savefig(tmpFile, dpi=200)
  pixBuf = gtk.gdk.pixbuf_new_from_file(tmpFile)
  cb = gtk.Clipboard()
  cb.set_image(pixBuf)
  os.remove(tmpFile)

def _addButton(tb, label, callback, fig, tooltip):
  button = gtk.Button(label)
  button.connect('clicked', callback, fig)
  button.set_tooltip_text(tooltip)
  ti = gtk.ToolItem()
  ti.add(button)
  tb.insert(ti, 0)

def _addCustomToolbar(fig):
  #fig.canvas.toolbar = CustomToolbar(fig.canvas, fig)
  # Start location varies depending on version, so you might want to change
  # this value.
  tb = fig.canvas.toolbar

  if useGtk:
    # Change axis
    a = gtk.Entry(40)
    ti = gtk.ToolItem()
    ti.add(a)
    #ti.set_visible(True)
    #a.set_visible(True)
    ti.show_all()
    a.connect('activate', _changeAxis, fig)
    a.set_editable(True)
    a.set_text('auto')
    a.set_tooltip_text("Change the axis:\n'on', 'off', 'equal', 'tight', 'auto'\n'x:xmin,xmax', 'y:ymin,ymax'\n'xmin,xmax,ymin,ymax'")
    a.grab_focus()
    tb.insert(ti, 0)

    _addButton(tb, 'Clip', _copyToClipboard, fig, 'Copy figure to system clipboard')

    tb.update()
    tb.show_all()
    fig.canvas.draw()

