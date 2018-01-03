import numpy as np
from framework import data
from .. import TestCaseEx

class TestEncoders(TestCaseEx):
  def test_converter(self):
    D = [
        ('hello', 'hello',),
        ('1', 1,),
        ('-3', -3,),
        ('1.0', 1.0,),
        ('true', True,),
        ('false', False,),
        ('1+3', '1+3',),
        ('[1, 6.0]', [1, 6.0],),
    ]
    for a, b in D:
      self.assertEqual(data.converter(a), b)
      self.assertEqual(data.inverse_converter(b), a)

  def test_vectorize_encoder(self):
    class TestEncoder(data.VectorizeEncoder):
      def __init__(self):
        super().__init__()
        self._fitted = set()

      def _fit(self, x):
        self._fitted.add(x)

      def _transform(self, x):
        return x if x in self._fitted else 0
    test = TestEncoder()
    test.fit([1, 2, 3])
    self.assertEqual(test._fitted, set([1, 2, 3]))
    self.assertNumpyEqual(test.transform(
        [1, 2, 3, 4, 5]), np.array([1, 2, 3, 0, 0]))

  def test_bool_encoder(self):
    boolEnc = data.BoolEncoder()
    self.assertNumpyEqual(
        boolEnc.transform([True, False, False, True]),
        np.array([1, 0, 0, 1]))

  def test_str_encoder(self):
    strEnc = data.StrEncoder()
    self.assertNumpyEqual(
        strEnc.fit_transform(['test 1', 'test 2', 'test 3', 'test 2']),
        np.array([0, 1, 2, 1]))

  def test_autodetect_encoder(self):
    le1 = data.AutodetectEncoder()
    test1 = np.array(['1', '2', '3', '4', '5'])
    test1_transformed = le1.fit_transform(test1)
    self.assertEqual(le1.dtype, int)
    self.assertEqual(le1.converter, True)
    self.assertNumpyEqual(test1_transformed, np.array([1, 2, 3, 4, 5]))
    self.assertNumpyEqual(le1.inverse_transform(test1_transformed), test1)

    le2 = data.AutodetectEncoder()
    test2 = np.array(['test 1', 'test 2', 'test 3', 'test 2', ' test 5'])
    test2_transformed = le2.fit_transform(test2)
    self.assertEqual(le2.dtype, str)
    self.assertEqual(le2.converter, False)
    self.assertNumpyEqual(test2_transformed, np.array([0, 1, 2, 1, 3]))
    self.assertNumpyEqual(le2.inverse_transform(test2_transformed), test2)

    le3 = data.AutodetectEncoder()
    test3 = np.array(['true', 'false'])
    test3_transformed = le3.fit_transform(test3)
    self.assertEqual(le3.dtype, bool)
    self.assertEqual(le3.converter, True)
    self.assertNumpyEqual(test3_transformed, np.array([1, 0]))
    self.assertNumpyEqual(le3.inverse_transform(test3_transformed), test3)

    le4 = data.AutodetectEncoder()
    test4 = np.array([1.0, 2.0])
    test4_transformed = le4.fit_transform(test4)
    self.assertEqual(le4.dtype, float)
    self.assertEqual(le4.converter, False)
    self.assertNumpyEqual(test4_transformed, test4)
    self.assertNumpyEqual(le4.inverse_transform(test4_transformed), test4)
