# Fairleigh Dickinson University Datamining Framework

[![Coverage Status](https://coveralls.io/repos/github/fdudatamining/framework/badge.svg?branch=master)](https://coveralls.io/github/fdudatamining/framework?branch=master)
[![Build Status](https://travis-ci.org/fdudatamining/framework.svg?branch=master)](https://travis-ci.org/fdudatamining/framework)

## Installation

### Release Installation

```
pip install https://github.com/fdudatamining/framework/archive/master.zip
```

### Bleeding Edge Installation

```
pip install https://github.com/fdudatamining/framework/archive/develop.zip
```

### Development Installation

It's recommended that you install the relevant packages for the framework in a virtual environment
```
git clone https://github.com/fdudatamining/framework
cd framework
virtualenv env
source env/bin/activate
python setup.py develop
```

## Framework Outline

This outline and framework is very much a draft, please don't expect to framework to work too much magic before it is complete. In particular, the model and process modules are currently in development, data has a few known issues with some conversions, but draw should work quite well.

### framework.data

Contains data preprocessing wrappers, primarily working with pandas dataframes and sklearn encoders. Much still needs to be done. Note that the wrapper will encode any strings making it very quick to have data ready for sklearn models. The results can then be inverted so that we know the actual prediction, not the encoded version.

Example:

```python
from framework.data import *

data = PandasData(pd.read_csv('data.csv'))
clf = SVC(); clf.fit(data.data().drop('Target'), target.data()['Target'])
data.invert(pd.concat([data.data(), clf.predict(data.data())]))
```

We've also added a simple wrapper for our clean in-house database.

```python
from framework.data import *
df = pd.read_sql('select * from hospitals', sql('datamining')))
```

### framework.draw

Contains specific plotting functionality designed for different models, the plotting wraps matplotlib plotting making for a much quicker and simpler way of plotting and extending plotting functionality. For a list of all the drawing types see `framework.draw.draw_kinds`

Example:

```python
from framework.draw import *

draw(title='Exponential', xlabel='t', ylabel='$e^t$',
     kind='plot', y=np.exp(range(10)))

x=np.linspace(0, 10)
for n in range(10):
  draw(kind='plot', x=x, y=[n*t for t in x],
       label='$%dt$' % (n))
draw(title='$nt$', xlabel='t', ylabel='y', legend='right', show=True, save='%d.png')
```

### framework.process

Contain high level querying of data leveraging some of the framework's models including: outlier/anomaly detection of points and trends, correlation (or lack-their-of) search via combinatorial groupby, common analytic pipeline wrappers, and sampling facilities.
