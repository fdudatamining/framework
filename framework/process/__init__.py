import pandas as pd
import numpy as np
import itertools as it
from sklearn import    \
    feature_selection, \
    model_selection,   \
    linear_model,      \
    neighbors,         \
    cluster

from .tunable import *

def outlier_detector(X, y,
                     selector=feature_selection.SelectKBest,
                     cv=model_selection.StratifiedKFold,
                     regressor=linear_model.LinearRegression,
                     distance=lambda d: neighbors.DistanceMetric.get_metric("mahalanobis", V=np.cov(d)),
                     threshold=3.0):
  '''
  1. selector returns most relevant features in data
  2. cross validator splits data into folds and trains regressor on data
  3. Errors calculated with mahalanobis distance metric
  3. Data with z scores above our threshold is generated
  '''
  selector = selector(k='all')#min(10, len(X))
  relevant_data = selector.fit_transform(X, y)
  cv = cv(relevant_data)
  regressor = regressor()
  mean_value_line = model_selection.cross_val_predict(regressor, relevant_data, cv=cv)
  distance = distance(mean_value_line)
  error = distance.pairwise(mean_value_line.predict(relevant_data), relevant_data)
  return data[(error-error.mean())/error.std() > threshold]


def iterative_kmeans(X, z=0.01, n_clusters=8, **kwargs):
  '''
  Process X with KMeans yielding rows that appear in lower than m-z
   clusters, and recursively processing on higher than m+z clusters.
  '''
  while len(X) != 0:
    km = cluster.KMeans(n_clusters=min(len(X), n_clusters), **kwargs)
    x = km.fit_predict(X)
    c = pd.value_counts(x).sort_values()
    thresh = c.mean() - z*c.std()
    ind = c[c < thresh].index
    if len(ind) != 0:
        yield(X[x==i] for i in ind)
    else:
        break
    X = X[np.in1d(x, c[c >= thresh].index)]

def aggregate_bins(df=None, x=None, y=None, z=None, n=10, aggfunc=None, fillna=np.NaN):
  ''' 3d binning view that lays out x and y binned in 2 dimensions and then the count in the bins
  as a color in the z direction or a custom z field and custom `aggfunc` for that field.
  To plot use:
    df = aggregate_bins(...)
    draw(kind='heatmap', df=df, clabel='Count', show=True)
  '''
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
  return g[z].agg(aggfunc).reset_index() \
          .pivot_table(index=y, columns=x, values=z) \
          .fillna(fillna)

def polyfit(*kargs):
  ''' A simple wrapper for np.polyfit that returns a more useful object '''
  return np.poly1d(
    np.polyfit(
      *kargs
    ))
