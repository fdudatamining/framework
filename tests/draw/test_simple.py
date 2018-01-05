import numpy as np
import pandas as pd
from unittest import TestCase
from framework import draw

X = np.array([1, 2, 3, 4, 5])

class TestSimplePlots(TestCase):
  def test_kinds(self):
    self.assertIsNotNone(draw.draw_kinds)

  def test_line(self):
    draw.draw(clear=True, kind='line', x=X, y=X)
    draw.draw(clear=True, kind='line', y=X)
  
  def test_scatter(self):
    draw.draw(clear=True, kind='scatter', x=X, y=X)
    draw.draw(clear=True, kind='scatter', y=X)

  def test_stem(self):
    draw.draw(clear=True, kind='stem', x=X, y=X)
    draw.draw(clear=True, kind='stem', y=X)

  def test_errorbar(self):
    draw.draw(clear=True, kind='errorbar', x=X, y=X, xerr=X, yerr=X)
    draw.draw(clear=True, kind='errorbar', y=X, yerr=X)

  def test_boxplot(self):
    draw.draw(clear=True, kind='boxplot', x=X)
  
  def test_barplot(self):
    draw.draw(clear=True, kind='barplot', x=X, y=X, width=1)
    draw.draw(clear=True, kind='barplot', x=X, y=X)
    draw.draw(clear=True, kind='barplot', y=X)

  def test_contour(self):
    draw.draw(clear=True, kind='contour', z=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
  
  def test_hist(self):
    draw.draw(clear=True, kind='hist', x=X, bins=2)
    draw.draw(clear=True, kind='hist', x=X)
