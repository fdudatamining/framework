import pandas as pd
from .encoders import AutodetectEncoder

class PandasData:
    ''' We process pandas dataframes with custom encoders, making it easy to get our data back '''

    def encode(self, data, **kwargs):
        ''' Given data, we encode it with the given encoders '''
        self._data = data.copy()
        self._encoders = {}
        for col in self._data.columns:
            dtype = self._data[col].dtype
            encoder = kwargs.get(col, AutodetectEncoder)
            self._encoders[col] = encoder()
            self._data[col] = self._encoders[col].fit_transform(self._data[col])
        # self._encoder = preprocessing.StandardScaler()
        # self._data.ix[:] = self._encoder.fit_transform(self._data)
    __init__ = encode  # we just use encoder as the constructor

    def invert(self, df):
        ''' Given encoded data, we should return a data frame with the original data '''
        for col in df.columns:
            encoder = self._encoders.get(col)
            if encoder:
                df[col] = encoder.inverse_transform(df[col])
        return df

    def data(self):
        return self.invert(self.df())

    def df(self, keep_cols=None, drop_cols=None):
        if keep_cols is not None:
            return self._data[keep_cols]
        elif drop_cols is not None:
            return self._data.drop(drop_cols, axis=1)
        else:
            return self._data.copy()
    
    def __str__(self):
        return '%s(_encoders=%s)' % (self.__class__.__name__, str(self._encoders))
    __repr__ = __str__
    