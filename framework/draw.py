'''
Draw module does everything through the draw function.

Usage:
  from framework.draw import draw
  # anything you would have put in different places for matplotlib
  # one line
  draw(title='Exponential', xlabel='t', ylabel='$e^t$',
     kind='plot', y=np.exp(range(10)))
  # multiline
  x=np.linspace(0, 10)
  for n in range(10):
    draw(kind='plot', x=x, y=[n*t for t in x],
       label='$%dt$' % (n))
  draw(title='$nt$', xlabel='t', ylabel='y', legend='right')

'''
import os
import re
import itertools as it
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import colors

# enumerate draw kinds
draw_kinds = [k[1:] for k in locals().keys()
              if re.match(r'^_[^_]', k)]

# inline mode supported
if 'inline' in matplotlib.get_backend():
    import plotly.offline as py
    py.init_notebook_mode(connected=True)

def cmap(seed):
  np.random.seed(seed)
  return colors.ListedColormap(np.random.rand(256, 3))

def draw(ax=None, kind=None, save=None, show=False, iplot=False, **kwargs):
  ''' Inline MATPLOTLIB functionality
  @parameters
   ax: plt axis (default None)
   kind: (see draw_kinds for available kinds) (default None)
   save: fname or format (e.g. fig%d.png) (default None)
   show: plt.show (default False)
   x, y: data (default None)
   grid: 'x', 'y', 'both' (default None)
   subplot: layout (default 111)
   xlabel, ylabel: str (default None)
   xmargin, ymargin: size (default 0.1)
   xlim, ylim: (min, max) (default auto)
   scientific: True, False, 'x', 'y' (default False)
   legend: True, 'right', 'bottom' (default None)
   kwargs: extra named args passed to matplotlib functions
  @return ax
  '''
  ax = ax or __subplot(**kwargs)
  if kind:
    eval('_%s' % (kind))(ax, **kwargs)
  __legend(ax, **kwargs)
  if save:
    __save(ax, save, **kwargs)
  if show:
    __show(ax)
  if iplot:
    __iplot(ax, **kwargs)
  if iplot or save or show:
    plt.clf()
  return ax


# Utility functions


def __nargs(args, **kwargs):
  ''' Filter **kwargs removing nulls and args we don't want '''
  return {k: v for k, v in kwargs.items()
          if v is not None and k in args}


def __subplot(grid=None, subplot=111,
              xlabel=None, ylabel=None,
              xmargin=0.1, ymargin=0.1,
              xlim=None, ylim=None,
              title=None, log=None,
              scientific=False, **kwargs):
  ax = plt.subplot(subplot)
  if grid:
    ax.grid(True, which=grid, **__nargs(['linestyle'], **kwargs))
  if title:
    ax.set_title(title)
  if xlabel:
    ax.set_xlabel(xlabel)
  if ylabel:
    ax.set_ylabel(ylabel)
  if xlim:
    ax.set_xlim(xlim)
  if ylim:
    ax.set_ylim(ylim)
  if xmargin or ymargin:
    ax.margins(**__nargs(['x', 'y'], x=xmargin, y=ymargin))
  if log:
    if log=='loglog':
      ax.loglog()
    elif log=='x' or log=='semilogx':
      ax.semilogx()
    elif log=='y' or log=='semilogy':
      ax.semilogy()
  # if scientific is not None:
  #   if scientific=='x':
  #     ax.get_yaxis().get_major_formatter().set_scientific(False)
  #   elif scientific=='y':
  #     ax.xaxis.get_major_formatter().set_scientific(False)
  #   else:
  #     ax.yaxis.get_major_formatter().set_scientific(scientific)
  #     ax.xaxis.get_major_formatter().set_scientific(scientific)
  return ax


def __legend(ax, legend=None, **kwargs):
  legend_sig = ['labels', 'loc', 'bbox_to_anchor']
  if legend == True:
    ax.legend(**__nargs(legend_sig, **kwargs))
  elif legend == 'bottom':
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height *
                      0.1, box.width, box.height * 0.9])
    ax.legend(**__nargs(legend_sig,
                        **dict(kwargs,
                               loc='upper center',
                               bbox_to_anchor=(0.5, -0.12))))
  elif legend == 'right':
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(**__nargs(legend_sig,
                        **dict(kwargs,
                               loc='center left',
                               bbox_to_anchor=(1.05, 0.5))))


def __save_fmt(fmt):
  if fmt.find('%d')!=-1:
    N = sorted(list(it.chain.from_iterable(
      [map(int, m.groups())
       for m in [re.match(fmt.replace('%d',r'(\d+)'), f)
                 for f in os.listdir('.')
                 if os.path.isfile(f)]
       if m])))
    R = N[-1]+1 if N else 0
    for i, n in enumerate(N):
      if i != n:
        R = i
        break
    return fmt % (R)
  return fmt


def __save(ax, fname, **kwargs):
  plt.savefig(__save_fmt(fname),
    **__nargs(['dpi', 'facecolor', 'edgecolor',
               'orientation', 'papertype', 'format',
               'transparent', 'bbox_inches', 'pad_inches',
               'frameon'],
              **dict(kwargs,
                     bbox_inches='tight',
                     bbox_extra_artists=ax.get_legend_handles_labels()[0] or None)))


def __show(ax, **kwargs):
  plt.show()

def __iplot(ax, **kwargs):
  py.iplot_mpl(ax.get_figure(),
    **__nargs(['scale',],
              **kwargs))


# Plot kinds

def _plot(ax, x=None, y=None, **kwargs):
  if x is None:
    x = range(len(y))
  ax.plot(x, y,
    **__nargs(['marker', 'c', 'label', 'linewidth'],
              **kwargs))


def _stem(ax, x=None, y=None, **kwargs):
  if x is None:
    x = range(len(y))
  ax.stem(x, y,
    **__nargs(['linefmt', 'markerfmt', 'basefmt',
               'label', 's', 'c',],
              **kwargs))


def _scatter(ax, x=None, y=None, **kwargs):
  if x is None:
    x = range(len(y))
  ax.scatter(x, y,
    **__nargs(['s', 'c', 'marker', 'cmap',
               'norm', 'vmin', 'vmax', 'alpha',
               'linewidths', 'verts',],
              **kwargs))


def _errorbar(ax, x=None, y=None, **kwargs):
  if x is None:
    x = range(len(y))
  ax.errorbar(x, y,
    **__nargs(['label', 'xerr', 'yerr', 'fmt', 'ecolor',
               'elinewidth', 'capsize', 'barsabove',
               'lolims', 'uplims', 'xlolims', 'xuplims',
               'errorevery', 'capthick', 'agg_filter',
               'alpha', 'animated', 'antialiased', 'axes',
               'clip_box', 'clip_on', 'clip_path', 'color',
               'contains', 'dash_capstyle', 'dash_joinstyle',
               'dashes', 'drawstyle', 'figure', 'fillstyle',
               'gid', 'label', 'linestyle', 'linewidth',
               'marker', 'markeredgecolor', 'markeredgewidth',
               'markerfacecolor', 'markerfacecoloralt',
               'markersize', 'markevery', 'path_effects',
               'picker', 'pickradius', 'rasterized',
               'sketch_params', 'snap', 'solid_capstyle',
               'solid_joinstyle', 'transform', 'url',
               'visible', 'xdata', 'ydata', 'zorder',],
              **kwargs))


def _boxplot(ax, x=None, **kwargs):
  ax.boxplot(x,
    **__nargs(['notch', 'sym', 'vert', 'whis',
               'positions', 'widths', 'patch_artist',
               'bootstrap', 'usermedians', 'conf_intervals',
               'meanline', 'showmeans', 'showcaps',
               'showbox', 'showfliers', 'boxprops', 'labels',
               'flierprops', 'medianprops', 'meanprops',
               'capprops', 'whiskerprops', 'manage_xticks',],
              **kwargs))

def _bar(ax, left=None, height=None, log=None, **kwargs):
  if log is not None:
    log = True
  ax.bar(left, height,
    **__nargs(['width', 'bottom', 'color', 'orientation', 'log',
               'edgecolor', 'linewidth', 'tick_label', 'xerr',
               'yerr', 'ecolor', 'capsize', 'error_kw', 'align',
               'agg_filter', 'alpha', 'animated', 'antialiased',
               'axes', 'capstyle', 'clip_box', 'clip_on',
               'clip_path', 'color', 'contains', 'edgecolor',
               'facecolor', 'figure', 'fill', 'gid', 'hatch',
               'joinstyle', 'label', 'linestyle', 'linewidth',
               'path_effects', 'picker', 'rasterized',
               'sketch_params', 'snap', 'transform', 'url',
               'visible', 'zorder',],
               **kwargs, log=log))

def _barh(ax, bottom=None, width=None, **kwargs):
  ax.bar(bottom, width,
    **__nargs(['height', 'left', 'color', 'edgecolor',
               'linewidth', 'tick_label', 'xerr', 'yerr',
               'ecolor', 'capsize', 'error_kw', 'align',
               'log', 'agg_filter', 'alpha', 'animated',
               'antialiased', 'axes', 'capstyle', 'clip_box',
               'clip_on', 'clip_path', 'color', 'contains',
               'edgecolor', 'facecolor', 'figure', 'fill',
               'gid', 'hatch', 'joinstyle', 'label', 'linestyle',
               'linewidth', 'path_effects', 'picker', 'rasterized',
               'sketch_params', 'snap', 'transform', 'url',
               'visible', 'zorder', ], **kwargs))



def _contourf(ax, x=None, y=None, z=None, **kwargs):
  ax.contourf(x, y, z,
    **__nargs(['marker', 'cmap', 'alpha'],
              **kwargs))

def _hist(ax, x=None, **kwargs):
  ax.hist(x,
    **__nargs(['bins', 'range', 'normed', 'weights',
               'cumalative', 'bottom', 'histtype', 'align',
               'orientation', 'rwidth', 'log',
               'color', 'label', 'stacked', 'hold',
               'linewidth', 'edgecolor',],
              **kwargs))


# Non-trivial drawing routines

def _svc(ax, clf=None, x=None, y=None, h=0.02, alpha=0.8, cmap=plt.cm.Paired, **kwargs):
  ''' http://scikit-learn.org/stable/auto_examples/svm/plot_iris.html '''
  x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
  y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
  xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
             np.arange(y_min, y_max, h))
  z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
  z = z.reshape(xx.shape)
  _contourf(ax, xx, yy, z, cmap=cmap, alpha=alpha)
  _scatter(ax, x[:, 0], x[:, 1], c=y, cmap=cmap)

def _linear_regression(ax, x=None, y=None, c=None, **kwargs):
  if c is None:
    c = next(ax._get_lines.color_cycle)
  z = np.polyfit(x, y, 1)
  p = np.poly1d(z)
  _scatter(ax, x=x, y=y, c=c, **kwargs)
  _plot(ax, x=x, y=p(x), c=c, **kwargs)
  return p

def _qq(ax, x=None, **kwargs):
  from scipy.stats import probplot
  probplot(y, dist='norm', plot=ax, **kwargs)

def _pca_variance(ax, pca=None, **kwargs):
  _plot(y=pca.explained_variance_, **kwargs)


# Other drawing routines outside of draw

def aggregate_bins(df=None, x=None, y=None, z=None, n=10, aggfunc=None, fillna=np.NaN, clabel='Count', **kwargs):
  ''' 3d binning view that lays out x and y binned in 2 dimensions and then the count in the bins
  as a color in the z direction or a custom z field and custom `aggfunc` for that field. '''
  if type(n) == int:
    # Support different x and y binning, if an iterable
    #  isn't passed, we turn it into an iterable.
    n = [n, n]
  if z is None:
    # Yes it's hacky, I know. This is required when a count is expected and z isn't
    #  necessary.
    if aggfunc is None:
      aggfunc = 'count'
    z = '_'
    df = df[[x, y]]
    df[z] = 1
  elif aggfunc is None:
    aggfunc = 'mean'
  gx, gy = [pd.cut(df[g], c) for g, c in zip([x,y], n)]
  # right edges of bins for ticks,
  # note that pandas uses strings to represent the cuts so we need to parse those
  g = df.groupby([gx, gy])
  a = g[z].agg(aggfunc).reset_index() \
          .pivot_table(index=y, columns=x, values=z) \
          .fillna(fillna)
  plt.imshow(a.values,
             origin='low', aspect='auto',
             interpolation='none',
             extent=(
                 float(a.columns[0].split(',')[0][1:]),
                 float(a.columns[-1].split(',')[1][1:-1]),
                 float(a.index[0].split(',')[0][1:]),
                 float(a.index[-1].split(',')[1][1:-1])),
             **__nargs(['origin', 'aspect', 'interpolation', 'extent'],
              **kwargs))
  cbar = plt.colorbar(shrink=.92)
  if clabel:
    cbar.set_label(clabel,
      **__nargs(['labelpad', 'y', 'rotation'],
        labelpad=-40, y=1.1, rotation=0, **kwargs))
  draw(**kwargs)
  return a

