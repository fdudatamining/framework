import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from unittest import TestCase
from framework import draw

class TestDraw(TestCase):
  def test_draw(self):
    # TODO: more thorough draw testing
    data = np.array([1, 2, 3, 4, 5])
    df = pd.DataFrame([[1,2,3,4,5], [2,3,4,5,1], [3,4,5,1,2,], [4,5,1,2,3,], [5,1,2,3,4,]])
    label = 'test'
    for kind in draw.draw_kinds:
      self.assertIsNotNone(
        draw.draw(kind=kind,
           df=df,
           x=data,
           y=data,
           z=data,
           left=data,
           right=data*2,
           height=data*2,
           bottom=data,
           label=label,
           xlabel=label,
           ylabel=label,
           zlabel=label,
           legend=True))
    draw.draw(kind='plot', x=data, y=data, legend='right')
    draw.draw(kind='plot', x=data, y=data, legend='bottom')
    draw.draw(kind='plot', x=data, y=data, scientific='x')
    draw.draw(kind='plot', x=data, y=data, scientific='y')
    draw.draw(kind='plot', x=data, y=data, scientific=True)

  def test_draw_clf(self):
    lr = LinearRegression()
    X = np.array([[1,2,], [4,5], [5,6]])
    y = np.array([1, 2, 3,])
    lr.fit(X, y)
    draw.draw(kind='decision_boundary', clf=lr, x=X, y=y)
