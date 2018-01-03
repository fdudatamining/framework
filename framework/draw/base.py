import os
import re
import itertools as it
import numpy as np

# Setup matplotlib
import matplotlib as mpl
if os.environ.get('DISPLAY', '') == '':
  print('no display found. Using non-interactive Agg backend')
  mpl.use('agg')

from matplotlib import pyplot as plt
from matplotlib import colors as mpl_colors

# inline mode supported
if 'inline' in mpl.get_backend():
  import plotly.offline as py
  py.init_notebook_mode(connected=True)
else:
  py = None

# kind registration decorator
draw_kinds = {}
def register(kind):
  def _register(obj):
    draw_kinds[kind] = obj
    return obj
  return _register

# primary function to build classes
def draw(kind='plot', **kwargs):
  return draw_kinds[kind](kind=kind, **kwargs)

# Util function
def nargs(l, omit=[]):
  ''' Usage:
  def wrapper_func(possible=None, args=None, **kwargs):
    wrapped_func(**nargs(locals()))
  
  This allows functions to be wrapped allowing arbitrary kwargs without breaking the underlying
   wrapped function by providing unnecessary arguments. Omit can be used if for-instance positional
   arguments are also being used.

  def wrapped_func(possible=None, args=None, **kwargs):
    wrapped_func(possible, **nargs(locals(), ['possible']))
  '''
  return {k:v for k,v in l.items()
          if k not in ['self', 'kwargs', *omit] and v is not None}

class Draw:
  def __init__(self, **kwargs):
    self.begin(**kwargs)
    self.render(**kwargs)
    self.end(**kwargs)

  def begin(self, **kwargs):
    pass

  def render(self, **kwargs):
    pass

  def end(self, **kwargs):
    pass

class Figure(Draw):
  def begin(self, ax=None, title=None,
            xlabel=None, ylabel=None,
            xlim=None, ylim=None,
            xmargin=None, ymargin=None,
            log=None, scientific=None,
            grid=None, **kwargs):
    if ax is not None:
      self.ax = ax
    elif getattr(self, 'ax', None) is None:
      self.subplot(**kwargs)

    if grid is not None:
      self.grid(b=True, which=grid, **kwargs)

    if title is not None:
      self.ax.set_title(title)

    if xlabel is not None:
      self.ax.set_xlabel(xlabel)
    if ylabel is not None:
      self.ax.set_ylabel(ylabel)

    if xlim is not None:
      self.ax.set_xlim(xlim)
    if ylim is not None:
      self.ax.set_ylim(ylim)

    if xmargin is not None or ymargin is not None:
      self.margins(x=xmargin, y=ymargin, **kwargs)

    if log == 'loglog':
      self.ax.loglog()
    elif log == 'x' or log == 'semilogx':
      self.ax.semilogx()
    elif log == 'y' or log == 'semilogy':
      self.ax.semilogy()

    if scientific == 'x':
      self.ax.get_xaxis().get_major_formatter().set_scientific(True)
      self.ax.get_yaxis().get_major_formatter().set_scientific(False)
    elif scientific == 'y':
      self.ax.get_xaxis().get_major_formatter().set_scientific(False)
      self.ax.get_yaxis().get_major_formatter().set_scientific(True)
    elif scientific is not None:
      self.ax.yaxis.get_major_formatter().set_scientific(scientific)
      self.ax.xaxis.get_major_formatter().set_scientific(scientific)
  
  def end(self, legend=None, cbar=None, **kwargs):
    if legend == 'bottom':
      box = self.ax.get_position()
      self.ax.set_position([box.x0, box.y0 + box.height *
                       0.1, box.width, box.height * 0.9])
      self.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), **kwargs)
    elif legend == 'right':
      box = self.ax.get_position()
      self.ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
      self.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), **kwargs)
    elif legend is not None:
      self.legend(**kwargs)

    if cbar is not None:
      self.cbar(cbar=cbar, **kwargs)
  
  def legend(self, labels=None, loc=None, bbox_to_anchor=None, **kwargs):
    self.ax.legend(**nargs(locals()))

  def cbar(self, cbar=None, clabel=None,
               clabel_pad=-40, clabel_y=1.1, clabel_rotation=0,
               cbar_shrink=0.92, **kwargs):
    if cbar is not None:
      self.colorbar(shrink=cbar_shrink, **kwargs)
      if clabel is not None:
        self.clabel(labelpad=clabel_pad, y=clabel_y, rotation=clabel_rotation, **kwargs)

  def colorbar(self, shrink=None, **kwargs):
    self.cbar = self.ax.colorbar(**nargs(locals()))

  def clabel(self, labelpad=None, y=None, rotation=None):
    self.cbar.set_label(**nargs(locals()))

  def subplot(self, nrows=1, ncols=1,
              sharex=False, sharey=False,
              subplot_kw=None, gridspec_kw=None,
              squeeze=True, num=None,
              figsize=None, dpi=None,
              facecolor=None, edgecolor=None,
              frameon=True,
              **kwargs):
    self.fig, self.ax = plt.subplots(**nargs(locals()))

  def grid(self, b=None, which=None, linestyle=None, **kwargs):
    self.ax.grid(**nargs(locals()))

  def margins(self, x=None, y=None, tight=None, **kwargs):
    self.ax.margins(**nargs(locals()))

class Display(Draw):
  def end(self, save=None, show=False, iplot=False, **kwargs):
    if save:
      self.save(save=save, **kwargs)

    if iplot:
      self.iplot(**kwargs)
    elif show:
      self.show(**kwargs)

    if iplot or save or show:
      self.clear(**kwargs)

  def save(self, save=None, **kwargs):
    self.savefig(
      fname=self.savefmt(
        save=save,
        **kwargs
      ),
      **kwargs
    )

  def savefig(self, fname=None, dpi=None, facecolor=None, edgecolor=None,
              orientation=None, papertype=None, format=None,
              transparent=None, bbox_inches='tight', pad_inches=None,
              frameon=None, bbox_extra_artists=None, **kwargs):
    if bbox_extra_artists is None:
      bbox_extra_artists = self.ax.get_legend_handles_labels()[0] or None
    plt.savefig(**nargs(locals()))

  def savefmt(self, save=None, **kwargs):
    if save.find('%d') != -1:
      N = sorted(list(it.chain.from_iterable(
          [map(int, m.groups())
          for m in [re.match(save.replace('%d', r'(\d+)'), f)
                    for f in os.listdir('.')
                    if os.path.isfile(f)]
          if m])))
      R = N[-1] + 1 if N else 0
      for i, n in enumerate(N):
        if i != n:
          R = i
          break
      return save % (R)
    return save

  def iplot(self, scale=None, **kwargs):
    if py is not None:
      py.iplot_mpl(self.ax.get_figure(), **nargs(locals()))
    else:
      print('WARN: iplot was specified but it could not be imported.')

  def show(self, block=None, **kwargs):
    plt.show(**nargs(locals()))

  def clear(self, **kwargs):
    plt.close()

@register('plot')
class Plot(Figure, Display):
  def begin(self, **kwargs):
    Figure.begin(self, **kwargs)
  
  def render(self, **kwargs):
    pass

  def end(self, **kwargs):
    Display.end(self, **kwargs)
