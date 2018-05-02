import numpy as np
import pandas as pd
from framework import process
from .. import TestCaseEx

class TestProcess(TestCaseEx):
  def test_outlier_detector(self):
    pass

  def test_iterative_kmeans(self):
    mat = np.array([
      [5,5,5,5,5,5,5,5,5,5,],
      [5,5,7,5,5,5,5,5,5,5,],
      [5,5,3,6,5,5,5,5,5,5,],
      [5,5,5,5,5,5,5,5,5,5,],
      [5,5,5,5,5,5,5,5,9,5,],
      [5,5,5,5,5,5,5,5,5,5,],
      [5,5,3,5,5,5,5,5,5,5,],
      [5,2,1,5,5,5,5,5,5,5,],
      [5,5,5,5,5,5,5,5,5,5,],
      [5,5,5,5,5,5,5,5,5,5,],
    ])
    for N in range(1, 10):
      for n, (inlier, outlier) in  enumerate(process.iterative_kmeans(mat, n_clusters=N)):
        self.assertNotEqual(mat[outlier].mean(), 5, 'Common row should not be an outlier')
        print(n, mat[outlier])

  def test_aggregate_bins1d(self):
    x = [1,2,2,3,3,3,4,4,4,4,5,5,5,5,5,]
    res = process.aggregate_bins1d(x, n=5)
    self.assertNumpyEqual(res.as_matrix(), np.array([1,2,3,4,5]))

  def test_aggregate_bins(self):
    df = pd.DataFrame([
      [1,2,3,],
      [2,3,4,],
      [3,4,5,],
      [4,5,6,],
      [5,6,7,],
      [6,7,8,],
      [7,8,9,],
      [8,9,8,],
      [9,8,7,],
    ], columns=[
      '1','2','3',
    ])
    res = process.aggregate_bins(df, x='1', y='2', z='3', n=9)
    self.assertEqual(res.sum().sum(), df['3'].sum())
    res = process.aggregate_bins(df, x='1', y='2', z='3', n=5, aggfunc='sum')
    self.assertEqual(res.sum().sum(), df['3'].sum())
    res = process.aggregate_bins(df, x='1', y='2', z='3', n=1, aggfunc='mean')
    self.assertEqual(res.sum().sum(), df['3'].mean())
    res = process.aggregate_bins(df, x='1', y='2', n=(3, 4))
    # TODO: explain why this is the transpose
    self.assertEqual(res.shape, (4, 3))
    # TODO: test for the location of high vs low values
