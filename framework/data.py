import os
import json
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sqlalchemy import create_engine

sql = lambda db: create_engine(
  json.load(
    open(os.path.expanduser('~/.sql.conf'), 'r'))['uri']+db)

def sql_to_csv(query, *args, script='%s/sql_to_csv.sh' % (os.path.abspath(os.path.dirname(__file__)))):
    ''' We execute this script in another thread after getting the temporary fifo and returning it
    that fifo can then be treated as a file for the output of the provided query. '''
    from threading import Thread
    from subprocess import Popen, PIPE
    p = Popen([script, *args], stdin=PIPE, stdout=PIPE)
    f = p.stdout.readline().strip().decode()
    t = Thread(target=p.communicate, kwargs={'input': query.encode()})
    t.start()
    return f

def converter(x):
    '''
    Magical converter--uses json magic.
    Useful for pd.read_csv(file, converters={'specialcol': converter})
     or df = df.apply(converter)
    '''
    if type(x) == str:
        try:
            v = json.loads(x)
            if type(v) == bool:
                v = 1 if v else 0
            return v
        except:
            pass
        return str(x)
    else:
        return x

class VectorizeEncoder:
    def __init__(self, x):
        self.fit = np.vectorize(self._fit)
        self.transform = np.vectorize(self._transform)

    def fit_transform(self, x):
        self.fit(x)
        return self.transform(x)

class BoolEncoder(VectorizeEncoder):
    def _fit(self, x):
        pass

    def _transform(self, x):
        return 1 if x else 0

class Encoder:
    '''
    Useful for PandasData encode_object.
    '''
    def __init__(self, type=None):
        self.encoder = None
        self.type = type

    def fit(self, x):
        ''' This depends on entries being a uniform type '''
        x = x.apply(converter)
        if not self.encoder:
            d = x[0]
            if not self.type:
                if type(d) == np.int64 or type(d) == np.float64 or type(d) == int or type(d) == float:
                    self.type = type(None)
                elif type(d) == list or type(d) == tuple:
                    self.type = type(list)
                elif type(d) == str:
                    self.type = type(str)
                elif type(d) == bool or type(d) == np.bool_:
                    self.type = type(bool)
                else:
                    print('Unexpected type: ', type(d), '\n', d)
            if self.type == str:
                self.encoder = preprocessing.LabelEncoder()
                x.fillna(str(), inplace=True)
            elif self.type == list:
                self.encoder = ListEncoder()
                x.fillna(list(), inplace=True)
            elif self.type == bool:
                self.encoder = BoolEncoder()

    def transform(self, x):
        return self.encoder.fit_transform(x) if self.encoder else x

    def fit_transform(self, x):
        self.fit(x)
        return self.transform(x)

    def inverse_transform(self, x):
        return self.encoder.inverse_transform(x) if self.encoder else x

class ListEncoder(Encoder):
    def __init__(self):
        parent().__init__(type)
        self.fit = np.vectorize(Encoder.fit)
        self.transform = np.vectorize(Encoder.transform)

class PandasData:
    ''' We process pandas dataframes with custom encoders, making it easy to get our data back '''

    def encode(self, data, **kwargs):
        ''' Given data, we encode it with the given encoders '''
        self._data = data
        self._encoders = {}
        for col in self._data:
            dtype = self._data[col].dtype
            encoder = kwargs.get(col, Encoder)
            self._encoders[col] = encoder()
            self._data[col] = self._encoders[col].fit_transform(self._data[col])
        self._encoder = preprocessing.StandardScaler()
        self._data = self._encoder.fit_transform(self._data)
    __init__ = encode  # we just use encoder as the constructor

    def invert(self, data):
        ''' Given ecoded data, we should return a data frame with the original data '''
        df = pd.DataFrame(columns=list(self._data))
        df.append(self._encoder.inverse_transform(data))
        for col in self._data:
            encoder = self._encoders.get(col)
            if encoder:
                df[col] = self._data[col].apply(encoder.inverse_transform)
            else:
                df[col] = self._data[col]
        return df

    def data(self):
        return self.invert(self._data)

    def df(self, cols=None, drop_cols=None):
        if keep_col is not None:
            return self._data[keep_col]
        elif drop_cols is not None:
            return self._data.drop(drop_col, axis=1)
        else:
            return self._data
