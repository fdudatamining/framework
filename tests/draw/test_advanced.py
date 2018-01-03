import os
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from unittest import TestCase
from framework import draw

X = np.array([
  [1, 2, 3, 4, 5],
  [2, 3, 4, 5, 6],
  [3, 4, 5, 6, 7],
  [4, 5, 6, 7, 8],
  [5, 6, 7, 8, 9],
])

y = np.array([
  1,
  2,
  3,
  4,
  5,
])

class TestAdvancedPlots(TestCase):
  def test_heatmap(self):
    draw.draw(kind='heatmap', df=pd.DataFrame(X))
  
  def test_decision_boundary(self):
    pass
    # clf = SVC()
    # clf.fit(X[:, :2], y)
    # draw.draw(kind='decision_boundary', clf=clf, x=X[:, 0], y=X[:, 1], y_true=y)

  def test_regression(self):
    draw.draw(kind='regression', x=y, y=y)
  
  def test_probplot(self):
    draw.draw(kind='probplot', x=y)
