useGtk = True
try:
    import gi
    gi.require_version('Gtk', '4.0')
    gi.require_version('Gdk', '4.0')
    from gi.repository import Gdk as gdk
    from gi.repository import Gtk as gtk
    from gi.repository import GdkPixbuf
except ImportError as e:
    useGtk = False
import matplotlib as mat
#mat.rcParams['toolbar'] = 'toolmanager'
#from matplotlib.backend_tools import ToolBase
import matplotlib.pyplot as plt
import os
import sys
import tempfile

def makeFigure():
    fig = plt.figure()
    #if plt.get_backend() in ('GTK3Agg', 'GTK3Cairo'):
    if False:
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
    #entry.grab_focus()

def _copyToClipboard(but, fig):
    # Note: this function does not allow copying between X clipboard and Windows,
    # which I think is an X limitation, and not a problem with the program itself.
    (fd, fn) = tempfile.mkstemp(suffix='.png')
    print('Temp file:', fn)
    fig.savefig(fn, dpi=200)
    pixBuf = GdkPixbuf.Pixbuf.new_from_file(fn)
    # This works for copying to other Ubuntu apps
    cb = gtk.Clipboard.get(gdk.SELECTION_CLIPBOARD)
    cb.set_image(pixBuf)
    os.close(fd)
    os.remove(fn)

def _changeBackground(but, fig):
    colorCycle = ([1, 1, 1], [0.75, 0.75, 0.75], [0.5, 0.5, 0.5], [0.25, 0.25, 0.25], [0, 0, 0])
    for ax in fig.axes:
        if hasattr(ax, '_currentBackgroundColor'):
            ax._currentBackgroundColor = (ax._currentBackgroundColor + 1) % len(colorCycle)
        else:
            ax._currentBackgroundColor = 0
        ax.set_facecolor(colorCycle[ax._currentBackgroundColor])
    fig.canvas.draw()

def _toggleGrid(but, fig):
    for ax in fig.axes:
        ax.grid()
    fig.canvas.draw()

def _addButton(tb, label, callback, fig, tooltip):
    button = gtk.Button(label)
    button.connect('clicked', callback, fig)
    button.set_tooltip_text(tooltip)
    ti = gtk.ToolItem()
    ti.add(button)
    tb.insert(ti, 0)

#class _ChangeBackground(ToolBase):
#    default_keymap = 'b'
#    description = 'Cycle background'
#    name = 'BG'
#    image = 'save'
#    def trigger(self, sender, event, data=None):
#        # self argument is not used
#        _changeBackground(self, sender)

def _addCustomToolbar(fig):
    #fig.canvas.toolbar = CustomToolbar(fig.canvas, fig)
    # Start location varies depending on version, so you might want to change
    # this value.
    tb = fig.canvas.toolbar

    # Old way of doing things with GTK
    if False:
        # Change axis
        a = gtk.Entry(max_length=40)
        ti = gtk.ToolItem()
        ti.add(a)
        #ti.set_visible(True)
        #a.set_visible(True)
        ti.show_all()
        a.connect('activate', _changeAxis, fig)
        a.set_editable(True)
        a.set_text('auto')
        a.set_tooltip_text("Change the axis:\n'on', 'off', 'equal', 'tight', 'auto'\n'x:xmin,xmax', 'y:ymin,ymax'\n'xmin,xmax,ymin,ymax'")
        #a.grab_focus()
        tb.insert(ti, 0)

        _addButton(tb, 'CP', _copyToClipboard, fig, 'Copy figure to system clipboard')
        _addButton(tb, 'BG', _changeBackground, fig, 'Cycle background color')
        _addButton(tb, 'GR', _toggleGrid, fig, 'Toggle on and off grid')

        tb.update()
        tb.show_all()
        fig.canvas.draw()
    else:
        # Matplotlib 3.5.1
        print('Adding BG tool.')
        fig.canvas.manager.toolbar.add_tool('BG', _ChangeBackground)

