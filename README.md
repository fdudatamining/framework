# Fairleigh Dickinson University Datamining Framework

[![Coverage Status](https://coveralls.io/repos/github/fdudatamining/framework/badge.svg?branch=develop)](https://coveralls.io/github/fdudatamining/framework?branch=develop)
[![Build Status](https://travis-ci.org/fdudatamining/framework.svg?branch=develop)](https://travis-ci.org/fdudatamining/framework)

## Framework Outline

This outline and framework is very much a draft, please don't expect to framework to work too much magic before it is complete. In particular, the model and process modules are currently in development, data has a few known issues with some conversions, but draw should work quite well.

### framework.data

Contains data preprocessing wrappers, primarily working with pandas dataframes and sklearn encoders. Much still needs to be done. Note that the wrapper will encode any strings making it very quick to have data ready for sklearn models. The results can then be inverted so that we know the actual prediction, not the encoded version.

Example:

```python
from framework.data import *

data = PandasData(pd.read_csv('data.csv'))
target = PandasData(pd.read_csv('target.csv'))
clf = SVC(); clf.fit(data.data, target.data)
print(*zip(data.invert(clf.predict(data.data)), target.invert(target.data)), sep='\n')
```

We've also added a simple wrapper for our clean in-house database.

```python
from framework.data import *
data = PandasData(pd.read_sql('select * from hospitals', sql))
```

### framework.draw

Contains specific plotting functionality designed for different models, the plotting wraps matplotlib plotting making for a much quicker and simpler way of plotting and extending plotting functionality.

Example:

```python
from framework.draw import draw

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

Example:

```python
from framework.process import *

for group, pt, stats in outlier_detector(pd.read_csv('data.csv'), limit_dimensions=2, threshold=4.0):
  print(group, pt, stats)
```
