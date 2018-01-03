import numpy as np
import pandas as pd
from unittest import TestCase
from framework import draw

X = np.array([1, 2, 3, 4, 5])

class TestSimplePlots(TestCase):
  def test_kinds(self):
    self.assertIsNotNone(draw.draw_kinds)

  def test_line(self):
    draw.draw(kind='line', x=X, y=X)
    draw.draw(kind='line', y=X)
  
  def test_scatter(self):
    draw.draw(kind='scatter', x=X, y=X)
    draw.draw(kind='scatter', y=X)

  def test_stem(self):
    draw.draw(kind='stem', x=X, y=X)
    draw.draw(kind='stem', y=X)

  def test_errorbar(self):
    draw.draw(kind='errorbar', x=X, y=X, xerr=X, yerr=X)
    draw.draw(kind='errorbar', y=X, yerr=X)

  def test_boxplot(self):
    draw.draw(kind='boxplot', x=X)
  
  def test_barplot(self):
    draw.draw(kind='barplot', x=X, y=X, width=1)
    draw.draw(kind='barplot', x=X, y=X)
    draw.draw(kind='barplot', y=X)

  def test_contour(self):
    pass
  
  def test_hist(self):
    draw.draw(kind='hist', x=X, bins=2)
    draw.draw(kind='hist', x=X)
