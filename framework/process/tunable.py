import itertools as it
import collections

def sorted_groupby(a, key=None):
  return it.groupby(sorted(a, key=key), key=key)
class Tunable:
  def __init__(self, *kargs, **kwargs):
    ''' First arg is obj if it's callable, else obj is None '''
    if len(kargs) == 0:
      kargs = [None]
    obj = kargs[0]
    if obj is None or callable(obj):
      self.obj = obj
      self.kargs = kargs[1:]
    else:
      self.obj = None
      self.kargs = kargs
    self.kwargs = kwargs

  def arg_type(arg):
    '''
      Simple type-comparison for determining if our key refers to
       a karg (int from enumerate) or a kwarg (string from dict key).
    '''
    key, val = arg
    return 'karg' if type(key) == int else 'kwarg'

  def group_args(args):
    '''
      Group args is a helper to restore a useable (karg, kwarg) pair format
       from the output of build_args.
      Given something that looks like this:
       [(0, 'First karg[0] option'), ('key', 'Random kwarg["key"] option')]
      We return something that looks like this:
       (['First karg[0] option'], {'key': 'Random kwarg["key"] option'})
    '''
    grouped = {typ: [g for g in groups]
               for typ, groups in sorted_groupby(args, key=Tunable.arg_type)}
    return ([v for k, v in sorted(grouped.get('karg', []))],
            {k: v for k, v in grouped.get('kwarg', [])})

  def handle_lookup(self, key, results, labels=False):
    '''
      Specific processing of results (allow us to convert karg -> kwarg if TunableChoice)
      When labels is true, each value is instead a (label, value) pair--we are looking up
       the value so we remove it.
    '''
    for v in results:
      if labels:
        v = v[1]
      yield (key, v)

  def build_args(self, lookup={}, labels=False):
    '''
      We gather all the kargs and kwargs in tuples (key, arg)
       where key is an integer for kargs and a string for kwargs.
      In the case of a Tunable we call handle_lookup to build
       potentially a list of possible args based on our already
       processed results available in the lookup dictionary.
      Args looks something like this:
      [
       [(0, 'First karg[0] option'), (0, 'Second karg[0] option')],
       [('key', 'Random kwarg["key"] option')],
       ...
      ]
      After calling it.product, we get something like this:
      [
       [(0, 'First karg[0] option'), ('key', 'Random kwarg["key"] option')],
       [(0, 'Second karg[0] option'), ('key', 'Random kwarg["key"] option')],
       ...
      ]
      Finally, after mapping group_args we end with this:
      [
       (['First karg[0] option'], {'key': 'Random kwarg["key"] option'}),
       (['Second karg[0] option'], {'key': 'Random kwarg["key"] option'}),
       ...
      ]
    '''
    args = []
    for key, arg in it.chain(enumerate(self.kargs), self.kwargs.items()):
      if isinstance(arg, Tunable):
        args.append(arg.handle_lookup(key, lookup[arg], labels=labels))
      else:
        args.append([(key, arg)])
    return map(Tunable.group_args, it.product(*args))

  def simplify_kargs_kwargs(self, *kargs, **kwargs):
    '''
      Simplification of kargs, kwargs allow the object to be
       somewhat seemless--that-is you can expect these outputs:
      Tunable(1) -> 1
      Tunable(1, 2) -> (1, 2)
      Tunable(a='b') -> dict(a='b')
      Tunable(1, a=b) -> (1, dict(a='b'))
    '''
    if kargs and kwargs:
      return (kargs, kwargs)
    elif kargs:
      if len(kargs) == 1:
        return kargs[0]
      else:
        return kargs
    elif kwargs:
      return kwargs

  def build_obj(self, *kargs, **kwargs):
    '''
      Call obj with available args or return them.
      If self.obj is set, we'll call it passing kargs and kwargs.
      If it isn't, then we simplify the data structure.
    '''
    if self.obj is not None:
      return self.obj(*kargs, **kwargs)
    else:
      return self.simplify_kargs_kwargs(*kargs, **kwargs)

  def evaluate(self, lookup={}, labels=False):
    '''
      Build kargs, kwargs, and pass them to the obj.
      Optionally, we can generate a (label, value) pair using
       the simplified kargs, kwargs.
    '''
    for kargs, kwargs in self.build_args(lookup=lookup, labels=labels):
      if labels:
        yield (
          self.simplify_kargs_kwargs(*kargs, **kwargs),
          self.build_obj(*kargs, **kwargs)
        )
      else:
        yield self.build_obj(*kargs, **kwargs)

  def build(self, labels=False):
    '''
      Walk returns all the objects from bottom to top, so we
       go through each object, evaluating each and making the
       possible results available to each parent Tunable.
      We support building  with labels to generate (label, value)
       pairs at each tunable step. Currently we only return the
       last label but in the future we might want to back-trace the
       evaluated dict and create a full label dict. All the relevant
       data to do this should already be available in the evaluated dict.
    '''
    evaluated = {}
    for obj in self.walk():
      evaluated[obj] = []
      for result in obj.evaluate(lookup=evaluated, labels=labels):
        if result not in evaluated[obj]:
          evaluated[obj].append(result)
    return evaluated[self]
  
  def __iter__(self):
    for res in self.build():
      yield res

  def walk(self):
    '''
      Depth first search to build processing order.
      This walks down the graph building a list in reverse (basically toposort).
      A closed list to eliminate duplicated nodes is
       not necessary because of how Tunables are assembled--
       if in the future however, cyclic Tunable dependencies
       are possible, the closed list can be uncommented.
    '''
    Q = collections.deque()
    P = collections.deque()
    # closed = set()
    Q.append(self)
    while Q:
      node = Q.pop()
      P.appendleft(node)
      for neighbor in node.neighbors():
        # if neighbor not in closed:
        Q.append(neighbor)
        # closed.add(neighbor)
    return P
  
  def neighbors(self):
    ''' Enumerate children Tunables for walk. '''
    for key, arg in it.chain(enumerate(self.kargs), self.kwargs.items()):
      if isinstance(arg, Tunable):
        yield arg

  def __hash__(self):
    ''' Object instance-unique hash function '''
    return id(self)

  def __eq__(self, other):
    ''' Object equality based on hash function '''
    return hash(self) == hash(other)

  def __ne__(self, other):
    ''' Opposite of __eq__ '''
    return not (self == other)

  def __repr__(self):
    ''' Representation that matches the call signature '''
    return '%s(%s)' % (
      self.obj.__name__ if self.obj is not None else '',
      ', '.join(
        it.chain(
          map(repr, self.kargs),
          ['='.join([str(k), repr(v)]) for k,v in self.kwargs.items()],
        )
      )
    )

class TunableChoice(Tunable):
  def evaluate(self, lookup={}, labels=False):
    ''' Build kargs, kwargs, and pass them to the obj '''
    for kargs, kwargs in self.build_args(lookup=lookup):
      for karg in kargs:
        kargs_ = [karg]
        if labels:
          yield (
            self.simplify_kargs_kwargs(*kargs_),
            self.build_obj(*kargs_)
          )
        else:
          yield self.build_obj(*kargs_)
      for key, kwarg in kwargs.items():
        kwargs_ = {key: kwarg}
        if labels:
          yield (
            self.simplify_kargs_kwargs(**kwargs_),
            self.build_obj(**kwargs_)
          )
        else:
          yield self.build_obj(**kwargs_)

  def handle_lookup(self, key, results, labels=False):
    ''' If dict, treat as kwarg in parent Tunable '''
    for v in results:
      if labels:
        v = v[1]
      if type(v) == dict:
        yield v.popitem()
      else:
        yield (key, v)

  def __repr__(self):
    ''' Understand choices with || (or) operator '''
    return '(%s)' % (' || '.join(
      it.chain(
        map(repr,self.kargs),
        ['%s=%s' % (k, repr(v)) for k,v in self.kwargs.items()]
      )
    ))

class TunableIterable(Tunable):
  def __init__(self, obj, *kargs, **kwargs):
    self.obj_iter = iter(obj)
    super().__init__(self.iter_func,
                     *kargs, **kwargs)

  def iter_func(self, *kargs, **kwargs):
      cur_obj = next(self.obj_iter)
      if callable(cur_obj):
        return cur_obj(*kargs, **kwargs)
      elif kargs and kwargs:
        return (cur_obj, kargs, kwargs)
      elif kargs:
        return (cur_obj, kargs)
      elif kwargs:
        return (cur_obj, kwargs)
      else:
        return cur_obj
