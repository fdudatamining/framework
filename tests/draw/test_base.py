import os
from unittest import TestCase
from framework import draw

class TestFigure(TestCase):
  def test_invalid_exception(self):
    with self.assertRaises(Exception) as context:
      draw.draw(kind='')
    self.assertTrue('is not a valid plot type' in str(context.exception))

  def test_ax(self):
    d=draw.draw()
    draw.draw(clear=True, ax=d.ax)
  
  def test_grid(self):
    draw.draw(clear=True, grid='both', axis='both')
    draw.draw(clear=True, grid='major', axis='x')
    draw.draw(clear=True, grid='minor', axis='y')

  def test_title(self):
    draw.draw(clear=True, title='test')

  def test_label(self):
    draw.draw(clear=True, xlabel='test')
    draw.draw(clear=True, ylabel='test')

  def test_lim(self):
    draw.draw(clear=True, xlim=(-1, 1))
    draw.draw(clear=True, ylim=(-1, 1))
  
  def test_margin(self):
    draw.draw(clear=True, xmargin=1)
    draw.draw(clear=True, ymargin=1)

  def test_log(self):
    draw.draw(clear=True, log='loglog')
    draw.draw(clear=True, log='x')
    draw.draw(clear=True, log='semilogx')
    draw.draw(clear=True, log='y')
    draw.draw(clear=True, log='semilogy')

  def test_scientific(self):
    draw.draw(clear=True, scientific='x')
    draw.draw(clear=True, scientific='y')
    draw.draw(clear=True, scientific=True)
    draw.draw(clear=True, scientific=False)

  def test_legend(self):
    draw.draw(clear=True, legend=True)
    draw.draw(clear=True, legend='bottom')
    draw.draw(clear=True, legend='right')
  
  def test_cbar(self):
    draw.draw(clear=True, cbar=True)
    draw.draw(clear=True, cbar=True, clabel=True)

class TestDisplay(TestCase):
  def test_save(self):
    draw.draw(clear=True, save='test.png')
    os.remove('test.png')

  def test_save_fmt(self):
    draw.draw(clear=True, save='test%d.png')
    os.remove('test0.png')

  def test_show(self):
    draw.draw(clear=True, show=True, block=False)
  
  def test_iplot(self):
    draw.draw(clear=True, iplot=True)
