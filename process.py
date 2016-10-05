import pandas as pd
import numpy as np
import itertools as it
from sklearn import *


def outlier_detector(data,
                     selector=feature_selection.SelectKBest,
                     cv=cross_validation.StratifiedKFold,
                     regressor=linear_model.LinearRegression,
                     distance=lambda d: neighbors.DistanceMetric.get_metric("mahalanobis", V=np.cov(d)),
                     threshold=3.0):
  '''
  1. selector returns most relevant features in data
  2. cross validator splits data into folds and trains regressor on data
  3. Errors calculated with mahalanobis distance metric
  3. Data with z scores above our threshold is generated
  '''
  selector = selector()
  relevant_data = selector.fit_transform(data)
  cv = cv(relevant_data)
  regressor = regressor()
  mean_value_line = cross_validation.cross_val_predict(regressor, relevant_data, cv=cv)
  distance = distance(mean_value_line)
  error = distance.pairwise(mean_value_line.predict(relevant_data), relevant_data)
  return data[(error-error.mean())/error.std() > threshold]
