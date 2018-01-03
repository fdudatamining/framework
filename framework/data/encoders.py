import json
import numpy as np

def converter(x):
    '''
    Magical converter--uses json magic.
    Useful for pd.read_csv(file, converters={'specialcol': converter})
     or df = df.apply(converter)
    '''
    if type(x) == str:
        try:
            return json.loads(x)
        except:
            pass
    return x

def inverse_converter(x):
    ''' Inverse of converter '''
    if type(x) != str:
        try:
            return json.dumps(x)
        except:
            pass
    return x


class VectorizeEncoder:
    def _fit(self, x):
        pass

    def fit(self, x):
        return np.vectorize(self._fit)(x)

    def _transform(self, x):
        pass

    def transform(self, x):
        return np.vectorize(self._transform)(x)

    def _inverse_transform(self, x):
        pass

    def inverse_transform(self, x):
        return np.vectorize(self._inverse_transform)(x)

    def fit_transform(self, x):
        self.fit(x)
        return self.transform(x)

    def __str__(self):
        return '%s' % (self.__class__.__name__)
    __repr__ = __str__

class BoolEncoder(VectorizeEncoder):
    def _fit(self, x):
        pass

    def _transform(self, x):
        return 1 if x else 0

    def _inverse_transform(self, x):
        return False if x == 0 else True


class StrEncoder(VectorizeEncoder):
    def __init__(self, classes={}):
        super().__init__()
        self.classes_ = classes
        self.inverse_classes_ = [i[1] for i in sorted(
            list(reversed(c)) for c in classes.items())]
        self.n_ = len(self.inverse_classes_)

    def _fit(self, x):
        assert type(x) == str or type(x) == np.str_, type(x)
        class_ = self.classes_.get(x, None)
        if class_ is None:
            self.classes_[x] = self.n_
            self.inverse_classes_.append(x)
            self.n_ += 1

    def _transform(self, x):
        assert type(x) == str or type(x) == np.str_, type(x)
        return self.classes_.get(x, None)

    def _inverse_transform(self, x):
        assert type(x) == int or type(x) == np.int64, type(x)
        return self.inverse_classes_[int(x)]

    def __str__(self):
        return '%s(n_=%d, classes_=%s)' % (self.__class__.__name__, self.n_, str(self.classes_))
    __repr__ = __str__

class AutodetectEncoder(VectorizeEncoder):
    '''
    A wrapper around encoders to provide encoder autodetection.
    '''

    def __init__(self, encoder=None, converter=None, dtype=None):
        super().__init__()
        self.converter = converter
        self.encoder = encoder
        self.dtype = dtype

    def _fit(self, x):
        ''' This depends on entries being a uniform type '''
        xc = converter(str(x) if type(x) == np.str_ else x)
        if self.converter is None:
            self.converter = xc != x
        if self.encoder is None:
            if self.dtype is None:
                if type(xc) == np.float64 or type(xc) == float:
                    self.dtype = float
                elif type(xc) == np.int64 or type(xc) == int:
                    self.dtype = int
                elif type(xc) == np.bool_ or type(xc) == bool:
                    self.dtype = bool
                elif type(xc) == np.str_ or type(xc) == str:
                    self.dtype = str
                else:
                    print('Unexpected type: ', xc, type(xc))
            if self.dtype == int or self.dtype == float:
                self.encoder = False
            elif self.dtype == str:
                self.encoder = StrEncoder()
            elif self.dtype == bool:
                self.encoder = BoolEncoder()
        return self.encoder._fit(xc) if self.encoder else xc

    def _transform(self, x):
        xc = converter(str(x)) if self.converter else x
        return self.encoder._transform(xc) if self.encoder else xc

    def _inverse_transform(self, x):
        xc = self.encoder._inverse_transform(x) if self.encoder else x
        return inverse_converter(xc) if self.converter else xc

    def inverse_transform(self, x):
        return np.vectorize(self._inverse_transform, otypes=[np.str_] if self.converter or self.dtype == str else None)(x)

    def __repr__(self):
        return '%s(dtype=%s, encoder=%s)' % (self.__class__.__name__, str(self.dtype), str(self.encoder))
