import matplotlib.pyplot as plt

def makeFigure():
  fig = plt.figure()
  can = fig.canvas
  tb = can.toolbar
  return fig
