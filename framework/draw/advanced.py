import numpy as np
from scipy import stats

from .base import *
from .simple import *

@register('heatmap')
class HeatmapPlot(Plot):
  def render(self, df=None, extent=None, **kwargs):
    if df is not None and extent is None:
      extent = (
          float(df.columns[0]),#.split(',')[0][1:]),
          float(df.columns[-1]),#.split(',')[1][1:-1]),
          float(df.index[0]),#.split(',')[0][1:]),
          float(df.index[-1]))#.split(',')[1][1:-1]))
    self.heatmap(X=df, extent=extent, **kwargs)

  def heatmap(self, X=None, extent=None, origin='low',
              aspect='auto', interpolation='none',
              cmap=None, norm=None, vmin=None, vmax=None,
              alpha=None, shape=None, filternorm=None,
              filterrad=None, **kwargs):
    self.ax.imshow(**nargs(locals()))

@register('decision_boundary')
class DecisionBoundaryPlot(ContourPlot, ScatterPlot):
  def render(self, clf=None, y_true=None, y_pred=None,
             x=None, y=None, alpha=0.8, cmap=plt.cm.Paired,
             p=0.5, h=0.02, **kwargs):
    xx, yy = np.meshgrid(np.arange(x.min() - p, x.max() + p, h),
                         np.arange(y.min() - p, y.max() + p, h))

    if clf is None:
      Z = y_pred(np.c_[xx.ravel(), yy.ravel()])
    elif hasattr(clf, 'decision_function'):
      Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    elif hasattr(clf, 'predict_proba'):
      Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    else:
      assert(False)

    Z = Z.reshape(xx.shape)

    ContourPlot.render(self, x=xx, y=yy, z=Z, cmap=cmap, alpha=alpha, **kwargs)
    ScatterPlot.render(self, x=x, y=y, color=y_true, cmap=cmap, **kwargs)
    # TODO: We'll need to override begin() to do this
    # if xlim is None:
    #   xlim = (xx.min(), xx.max())
    # if ylim is None:
    #   ylim = (yy.min(), yy.max())

@register('regression')
class RegPlot(ScatterPlot, LinePlot):
  def render(self, x=None, y=None, **kwargs):
    y_fit = np.poly1d(np.polyfit(x, y, 1))
    ScatterPlot.render(self, x=x, y=y, **kwargs)
    LinePlot.render(self, x=[min(x), max(x)], y=y_fit([min(x), max(x)]), **kwargs)

@register('probplot')
class ProbPlot(Plot):
  def render(self, x=None, **kwargs):
    self.probplot(x=x, plot=self.ax, **kwargs)

  def probplot(self, x=None, dist='norm', plot=None, **kwargs):
    stats.probplot(**nargs(locals()))

