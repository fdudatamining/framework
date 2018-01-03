import numpy as np

from .base import *

@register('line')
class LinePlot(Plot):
  def render(self, x=None, y=None, size=None, color='b', alpha=1, **kwargs):
    if x is None:
      x = range(len(y))
    self.line(x=x, y=y, s=size, c=color, alpha=alpha, **kwargs)
  
  def line(self, x=None, y=None, s=None, c=None, alpha=None,
           marker=None, cmap=None, norm=None,
           vmin=None, vmax=None, label=None,
           linewidths=None, verts=None, edgecolors=None,
           **kwargs):
    self.ax.plot(**nargs(locals()))

@register('scatter')
class ScatterPlot(Plot):
  def render(self, x=None, y=None, size=None, color='b', alpha=1, **kwargs):
    if x is None:
      x = range(len(y))
    self.scatter(x=x, y=y, s=size, c=color, alpha=alpha, **kwargs)
  
  def scatter(self, x=None, y=None, s=None, c=None, alpha=None,
              marker=None, cmap=None, norm=None, label=None,
              vmin=None, vmax=None, verts=None, edgecolors=None,
              **kwargs):
    self.ax.scatter(**nargs(locals()))

@register('stem')
class StemPlot(Plot):
  def render(self, x=None, y=None, size=None, color=None, alpha=1, **kwargs):
    self.stem(x=x, y=y, s=size, c=color, **kwargs)

  def stem(self, x=None, y=None,
           linefmt=None, markerfmt=None, basefmt=None,
           label=None, s=None, c=None, **kwargs):
    if x is None:
      self.ax.stem(y, **nargs(locals(), ['x', 'y']))
    elif y is None:
      self.ax.stem(x, y, **nargs(locals(), ['x', 'y']))

@register('errorbar')
class ErrorBarPlot(Plot):
  def render(self, x=None, y=None, xerr=None, yerr=None, size=None, color='b', alpha=1, **kwargs):
    if x is None:
      x = range(len(y))
    self.errorbar(x=x, y=y, s=size, c=color, alpha=alpha,
                  xerr=xerr, yerr=yerr, **kwargs)
  
  def errorbar(self, x=None, y=None, label=None, xerr=None, yerr=None,
               fmt=None, ecolor=None, elinewidth=None, capsize=None,
               lolims=None, uplims=None, xlolims=None, xuplims=None,
               errorevery=None, capthick=None, agg_filter=None,
               alpha=None, animated=None, antialiased=None, axes=None,
               clip_box=None, clip_on=None, clip_path=None, color=None,
               contains=None, dash_capstyle=None, dash_joinstyle=None,
               dashes=None, drawstyle=None, figure=None, fillstyle=None,
               gid=None, linestyle=None, linewidth=None, barsabove=None,
               marker=None, markeredgecolor=None, markeredgewidth=None,
               markerfacecolor=None, markerfacecoloralt=None,
               markersize=None, markevery=None, path_effects=None,
               picker=None, pickradius=None, rasterized=None,
               sketch_params=None, snap=None, solid_capstyle=None,
               solid_joinstyle=None, transform=None, url=None,
               visible=None, xdata=None, ydata=None, zorder=None, **kwargs):
    self.ax.errorbar(**nargs(locals()))

@register('boxplot')
class BoxPlot(Plot):
  def render(self, x=None, **kwargs):
    self.boxplot(x=x, **kwargs)
  
  def boxplot(self, x=None, notch=None, sym=None, vert=None, whis=None,
              positions=None, widths=None, patch_artist=None,
              bootstrap=None, usermedians=None, conf_intervals=None,
              meanline=None, showmeans=None, showcaps=None,
              showbox=None, showfliers=None, boxprops=None, labels=None,
              flierprops=None, medianprops=None, meanprops=None,
              capprops=None, whiskerprops=None, manage_xticks=None, **kwargs):
    self.ax.boxplot(**nargs(locals()))

@register('barplot')
class BarPlot(Plot):
  def render(self, x=None, y=None, height=None, width=None, vertical=False, **kwargs):
    if height is None:
      height = y
    if x is None:
      x = range(len(height))
    if width is None:
      width = np.min(np.diff(x))
    self.bar(x=x, height=height, width=width, **kwargs)

  def bar(self, x=None, height=None, width=None, bottom=None,
          tick_label=None, xerr=None, yerr=None, ecolor=None,
          agg_filter=None, alpha=None, animated=None, antialiased=None,
          axes=None, capstyle=None, clip_box=None, clip_on=None,
          clip_path=None, color=None, contains=None, edgecolor=None,
          facecolor=None, figure=None, fill=None, gid=None, hatch=None,
          joinstyle=None, label=None, linestyle=None, linewidth=None,
          path_effects=None, picker=None, rasterized=None, capsize=None,
          sketch_params=None, snap=None, transform=None, url=None,
          visible=None, zorder=None,  orientation=None, log=None,
          error_kw=None, align=None, **kwargs):
    self.ax.bar(x, height, width, **nargs(locals(), ['x', 'height', 'width']))

@register('contour')
class ContourPlot(Plot):
  def render(self, x=None, y=None, z=None, **kwargs):
    self.contourf(x=x, y=y, z=z, **kwargs)
  
  def contourf(self, x=None, y=None, z=None,
               marker=None, cmap=None, alpha=None,
               **kwargs):
    if x is None and y is None:
      self.ax.contourf(z, **nargs(locals(), ['x', 'y', 'z']))
    else:
      self.ax.contourf(x, y, z, **nargs(locals(), ['x', 'y', 'z']))

@register('hist')
class HistPlot(Plot):
  def render(self, x=None, **kwargs):
    self.hist(x=x, **kwargs)

  def hist(self, x=None, bins=None, range=None, normed=None, weights=None,
            cumalative=None, bottom=None, histtype=None, align=None,
            orientation=None, rwidth=None, log=None,
            color=None, label=None, stacked=None, hold=None,
            linewidth=None, edgecolor=None, **kwargs):
    self.ax.hist(**nargs(locals()))
