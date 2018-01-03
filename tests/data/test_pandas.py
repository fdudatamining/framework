import pandas as pd
from framework import data
from .. import TestCaseEx

class TestPandasData(TestCaseEx):
  def test_pandas_data(self):
    df = pd.DataFrame([
      [1, '1', 'test 1', True, 'false'],
      [2, '2', 'test 2', False, 'true'],
    ], columns=['nums', 'str_nums', 'strs', 'bools', 'str_bools',])
    df_expected = pd.DataFrame([
      [1, 1, 0, 1, 0],
      [2, 2, 1, 0, 1],
    ], columns=['nums', 'str_nums', 'strs', 'bools', 'str_bools',])
    df_wrapped = data.PandasData(df)
    df_wrapped_df = df_wrapped.df()
    df_wrapped_inverse = df_wrapped.data()
    for orig, expected, wrapped, wrapped_inverse in zip(df.iterrows(), df_expected.iterrows(), df_wrapped_df.iterrows(), df_wrapped_inverse.iterrows()):
      _, orig_row = orig
      _, expected_row = expected
      _, wrapped_row = wrapped
      _, wrapped_inverse_row = wrapped_inverse
      self.assertNumpyEqual(wrapped_row, expected_row)
      self.assertNumpyEqual(orig_row, wrapped_inverse_row)
