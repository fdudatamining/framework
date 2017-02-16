from unittest import TestCase
from framework import process

class TestProcess(TestCase):
  pass
# def outlier_detector(data,
#                      selector=feature_selection.SelectKBest,
#                      cv=cross_validation.StratifiedKFold,
#                      regressor=linear_model.LinearRegression,
#                      distance=lambda d: neighbors.DistanceMetric.get_metric("mahalanobis", V=np.cov(d)),
#                      threshold=3.0):
#   '''
#   1. selector returns most relevant features in data
#   2. cross validator splits data into folds and trains regressor on data
#   3. Errors calculated with mahalanobis distance metric
#   3. Data with z scores above our threshold is generated
#   '''
#   selector = selector()
#   relevant_data = selector.fit_transform(data)
#   cv = cv(relevant_data)
#   regressor = regressor()
#   mean_value_line = cross_validation.cross_val_predict(regressor, relevant_data, cv=cv)
#   distance = distance(mean_value_line)
#   error = distance.pairwise(mean_value_line.predict(relevant_data), relevant_data)
#   return data[(error-error.mean())/error.std() > threshold]


# def iterative_kmeans(X, z=0.01, n_clusters=8, **kwargs):
#   '''
#   Process X with KMeans yielding rows that appear in lower than m-z
#    clusters, and recursively processing on higher than m+z clusters.
#   '''
#   while len(X) != 0:
#     km = cluster.KMeans(n_clusters=min(len(X), n_clusters), **kwargs)
#     x = km.fit_predict(X)
#     c = pd.value_counts(x).sort_values()
#     thresh = c.mean() - z*c.std()
#     ind = c[c < thresh].index
#     if len(ind) != 0:
#         yield(X[x==i] for i in ind)
#     else:
#         break
#     X = X[np.in1d(x, c[c >= thresh].index)]
