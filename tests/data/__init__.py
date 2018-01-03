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
          np.equal(a, b).all(),
          '%s != %s' % (a, b))
    except:
      self.assertEqual(a.tolist(), b.tolist(), '%s != %s' % (a, b))
