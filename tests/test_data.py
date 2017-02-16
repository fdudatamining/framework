from unittest import TestCase
from framework import data

class TestDraw(TestCase):
  def test_converter(self):
    self.assertEqual(data.converter('hello'), 'hello')
    self.assertEqual(data.converter('1'), 1)
    self.assertEqual(data.converter('-3'), -3)
    self.assertEqual(data.converter('1.0'), 1.0)
    self.assertEqual(data.converter('.06'), 0.06)
    self.assertEqual(data.converter('1e5'), 1e5)
    self.assertEqual(data.converter('true'), True)
    self.assertEqual(data.converter('false'), False)
    self.assertEqual(data.converter('1+3'), '1+3')
    self.assertEqual(data.converter('[1, 6.0]'), [1, 6.0])

  def test_vectorize_encoder(self):
    class TestEncoder(data.VectorizeEncoder):
      def _fit(self, x):
        self._fitted = x
      def _transform(self, x):
        return str(x) if x in self._fitted else x
    test = TestEncoder()
    self.assertEqual(type(test.fit), np.lib.function_base.vectorize)
    self.assertEqual(type(test.transform), np.lib.function_base.vectorize)
    test.fit([1, 2, 3])
    self.assertEqual(test._fitted, np.array([1, 2, 3]))
    self.assertEqual(test.transform([1, 2, 3, 4, 5]), np.array(['1', '2', '3', 4, 5]))

  def test_bool_encoder(self):
    boolEnc = BoolEncoder()
    self.assertEqual(boolEnc.fit_transform([True, False, False, True]), np.array([1, 0, 0, 1]))

# class Encoder:
#     '''
#     Useful for PandasData encode_object.
#     '''
#     def __init__(self, type=None):
#         self.encoder = None
#         self.type = type

#     def fit(self, x):
#         ''' This depends on entries being a uniform type '''
#         x = x.apply(converter)
#         if not self.encoder:
#             d = x[0]
#             if not self.type:
#                 if type(d) == np.int64 or type(d) == np.float64 or type(d) == int or type(d) == float:
#                     self.type = type(None)
#                 elif type(d) == list or type(d) == tuple:
#                     self.type = type(list)
#                 elif type(d) == str:
#                     self.type = type(str)
#                 elif type(d) == bool or type(d) == np.bool_:
#                     self.type = type(bool)
#                 else:
#                     print('Unexpected type: ', type(d), '\n', d)
#             if self.type == str:
#                 self.encoder = preprocessing.LabelEncoder()
#                 x.fillna(str(), inplace=True)
#             elif self.type == list:
#                 self.encoder = ListEncoder()
#                 x.fillna(list(), inplace=True)
#             elif self.type == bool:
#                 self.encoder = BoolEncoder()

#     def transform(self, x):
#         return self.encoder.fit_transform(x) if self.encoder else x

#     def fit_transform(self, x):
#         self.fit(x)
#         return self.transform(x)

#     def inverse_transform(self, x):
#         return self.encoder.inverse_transform(x) if self.encoder else x

# class ListEncoder(Encoder):
#     def __init__(self):
#         parent().__init__(type)
#         self.fit = np.vectorize(Encoder.fit)
#         self.transform = np.vectorize(Encoder.transform)

# class PandasData:
#     ''' We process pandas dataframes with custom encoders, making it easy to get our data back '''

#     def encode(self, data, **kwargs):
#         ''' Given data, we encode it with the given encoders '''
#         self._data = data
#         self._encoders = {}
#         for col in self._data:
#             dtype = self._data[col].dtype
#             encoder = kwargs.get(col, Encoder)
#             self._encoders[col] = encoder()
#             self._data[col] = self._encoders[col].fit_transform(self._data[col])
#         self._encoder = preprocessing.StandardScaler()
#         self._data = self._encoder.fit_transform(self._data)
#     __init__ = encode  # we just use encoder as the constructor

#     def invert(self, data):
#         ''' Given ecoded data, we should return a data frame with the original data '''
#         df = pd.DataFrame(columns=list(self._data))
#         df.append(self._encoder.inverse_transform(data))
#         for col in self._data:
#             encoder = self._encoders.get(col)
#             if encoder:
#                 df[col] = self._data[col].apply(encoder.inverse_transform)
#             else:
#                 df[col] = self._data[col]
#         return df

#     def data(self):
#         return self.invert(self._data)

#     def df(self, cols=None, drop_cols=None):
#         if keep_col is not None:
#             return self._data[keep_col]
#         elif drop_cols is not None:
#             return self._data.drop(drop_col, axis=1)
#         else:
#             return self._data
