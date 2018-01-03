import os
from unittest import TestCase
from framework import draw

class TestFigure(TestCase):
  def test_ax(self):
    d=draw.draw()
    draw.draw(ax=d.ax)
  
  def test_grid(self):
    draw.draw(grid='both', axis='both')
    draw.draw(grid='major', axis='x')
    draw.draw(grid='minor', axis='y')

  def test_title(self):
    draw.draw(title='test')

  def test_label(self):
    draw.draw(xlabel='test')
    draw.draw(ylabel='test')

  def test_lim(self):
    draw.draw(xlim=(-1, 1))
    draw.draw(ylim=(-1, 1))
  
  def test_margin(self):
    draw.draw(xmargin=1)
    draw.draw(ymargin=1)

  def test_log(self):
    draw.draw(log='loglog')
    draw.draw(log='x')
    draw.draw(log='semilogx')
    draw.draw(log='y')
    draw.draw(log='semilogy')

  def test_scientific(self):
    draw.draw(scientific='x')
    draw.draw(scientific='y')
    draw.draw(scientific=True)
    draw.draw(scientific=False)

  def test_legend(self):
    draw.draw(legend=True)
    draw.draw(legend='bottom')
    draw.draw(legend='right')
  
  def test_cbar(self):
    draw.draw(cbar=True)
    draw.draw(cbar=True, clabel=True)

class TestDisplay(TestCase):
  def test_save(self):
    draw.draw(save='test.png')
    os.remove('test.png')

  def test_save_fmt(self):
    draw.draw(save='test%d.png')
    os.remove('test0.png')

  def test_show(self):
    draw.draw(show=True, block=False)
  
  def test_iplot(self):
    draw.draw(iplot=True)
