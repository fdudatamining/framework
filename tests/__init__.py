import numpy as np
from unittest import TestCase

class TestCaseEx(TestCase):
  def assertNumpyEqual(self, a: np.array, b: np.array):
    print('%s == %s ?' % (a, b))
    self.assertEqual(a.dtype, b.dtype,
                     '%s != %s' % (a.dtype, b.dtype))
    self.assertEqual(a.shape, b.shape,
                     '%s != %s' % (a.shape, b.shape))
    try:
      self.assertTrue(
        all([aa == bb for aa in a for bb in b]),
        '%s != %s' % (a, b))
    except:
      self.assertEqual(a.tolist(), b.tolist(), '%s != %s' % (a, b))

  def assertMatchAnyOrder(self, a, b, c=None):
    a = list(a)
    b = list(b)
    print('Comparing \n%s\n and \n%s' % (repr(a), repr(b)))
    self.assertEqual(len(a), len(b), 'len(%s) != len(%s)' % (repr(a), repr(b)))
    for aa in a:
      if aa not in b:
        self.fail('%s not in %s' % (repr(aa), repr(b)) if c is None else c)
    for bb in b:
      if bb not in a:
        self.fail('%s not in %s' % (repr(bb), repr(a)) if c is None else c)
