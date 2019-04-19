import time
import numpy as np
from .. import TestCaseEx
from framework.process import *

def dummy(*kargs, **kwargs):
  return (kargs, kwargs)

def any_sum(*kargs, **kwargs):
  return sum([*kargs, *kwargs.values()])

class TestTunable(TestCaseEx):
  def test_tunable_auto_none(self):
    self.assertMatchAnyOrder(
      Tunable(1, 2),
      [
        (1, 2,),
      ],
    )
    self.assertMatchAnyOrder(
      Tunable(a=3, b=4),
      [
        {'a':3, 'b':4},
      ],
    )
    self.assertMatchAnyOrder(
      Tunable(1, 2, a=3, b=4),
      [
        ((1, 2,), {'a':3, 'b':4}),
      ],
    )

  def test_tunable_callable_no_args(self):
    self.assertMatchAnyOrder(
      Tunable(lambda: 'test'),
      [
        'test'
      ],
    )

  def test_tunable_single(self):
    self.assertMatchAnyOrder(
      Tunable(dummy,
        1, 2, 3,
        a=4, b=5, c=6),
      [
        ((1,2,3), dict(a=4, b=5, c=6)),
      ],
    )

  def test_tunable_nested(self):
    self.assertMatchAnyOrder(
      Tunable(dummy,
        Tunable(dummy, 1,2,3),
        a=Tunable(dummy, a=4, b=5, c=6)
      ),
      [
        (
          (((1, 2, 3), dict()),),
          dict(a=((), dict(a=4, b=5, c=6)))
        ),
      ]
    )

  def test_auto_tunable_choice(self):
    self.assertMatchAnyOrder(
      TunableChoice(
        1, 2, 3
      ),
      [
        1,
        2,
        3,
      ],
    )
    self.assertMatchAnyOrder(
      TunableChoice(
        a=1,
        b=2,
        c=3
      ),
      [
        dict(a=1),
        dict(b=2),
        dict(c=3),
      ],
    )

  def test_tunable_choice(self):
    self.assertMatchAnyOrder(
      TunableChoice(
        Tunable(dummy, 1, 2, 3),
        Tunable(dummy, a=4, b=5, c=6),
      ),
      [
        ((1, 2, 3,), dict()),
        ((), dict(a=4, b=5, c=6)),
      ],
    )

  def test_tunable_choice_auto_kargs(self):
    self.assertMatchAnyOrder(
      Tunable(dummy,
        1, 2, TunableChoice(3, 4,)
      ),
      [
        ((1, 2, 3,), dict()),
        ((1, 2, 4,), dict()),
      ],
    )
    self.assertMatchAnyOrder(
      Tunable(dummy,
        c=TunableChoice(3, 4),
        a=1, b=2,
      ),
      [
        ((), dict(a=1, b=2, c=3)),
        ((), dict(a=1, b=2, c=4)),
      ],
    )

  def test_tunable_choice_product(self):
    self.assertMatchAnyOrder(
      Tunable(dummy,
        TunableChoice(1, 2, 3),
        TunableChoice(a=4, b=5, c=6),
      ),
      [
        ((1,), dict(a=4)),
        ((1,), dict(b=5)),
        ((1,), dict(c=6)),
        ((2,), dict(a=4)),
        ((2,), dict(b=5)),
        ((2,), dict(c=6)),
        ((3,), dict(a=4)),
        ((3,), dict(b=5)),
        ((3,), dict(c=6)),
      ],
    )
  
  def test_nested_tunable_choice(self):
    self.assertMatchAnyOrder(
      TunableChoice(
        a=TunableChoice(1, 2, 3),
        b=TunableChoice(4, 5, 6),
        c=TunableChoice(7, 8, 9),
      ),
      [
          dict(a=1),
          dict(a=2),
          dict(a=3),
          dict(b=4),
          dict(b=5),
          dict(b=6),
          dict(c=7),
          dict(c=8),
          dict(c=9),
      ],
    )

  def test_nested_combinations(self):
    self.assertMatchAnyOrder(
      Tunable(dummy,
        1, 2,
        a=Tunable(dummy,
          3, 4,
          b=TunableChoice(
            Tunable(dummy,
              TunableChoice(5, 6),
            ),
            Tunable(dummy,
              TunableChoice(7, 8),
            ),
          ),
        ),
      ),
      [
        ((1, 2,), {'a': ((3, 4,), {'b': ((5,), {})})}),
        ((1, 2,), {'a': ((3, 4,), {'b': ((6,), {})})}),
        ((1, 2,), {'a': ((3, 4,), {'b': ((7,), {})})}),
        ((1, 2,), {'a': ((3, 4,), {'b': ((8,), {})})}),
      ])

  def test_tunable_labels(self):
    self.assertMatchAnyOrder(
      Tunable(any_sum,
        1, 2,
        TunableChoice(
          3, 4, 5
        )
      ).build(labels=True),
      [
        ((1, 2, 3), 6),
        ((1, 2, 4), 7),
        ((1, 2, 5), 8),
      ])

  # def test_nested_tunable_choice_labels(self):
  #   self.assertMatchAnyOrder(
  #     Tunable(any_sum,
  #       a=Tunable(any_sum,
  #         1, 2, 3,
  #       ),
  #       b=Tunable(any_sum, 
  #         a=4, b=5, c=6,
  #       ),
  #       c=Tunable(any_sum,
  #         TunableChoice(7, 8, 9),
  #       ),
  #     ).build(labels=True),
  #     [
  #       (dict(a=1), 1),
  #       (dict(a=2), 2),
  #       (dict(a=3), 3),
  #       (dict(b=4), 4),
  #       (dict(b=5), 5),
  #       (dict(b=6), 6),
  #       (dict(c=7), 7),
  #       (dict(c=8), 8),
  #       (dict(c=9), 9),
  #     ])

  def test_tunable_iterable(self):
    for i, r in enumerate(TunableIterable(it.count())):
      self.assertEqual(i, r)
      if i > 10:
        break

  def test_tunable_iterable_args(self):
    t = Tunable(dummy,
      TunableIterable(it.count()),
      a=TunableIterable(it.count()),
    )
    for i, r in enumerate(t):
      self.assertEqual(
        ((i,), dict(a=i)),
        r
      )
      if i > 10:
        break

  def test_nested_tunable_iterable(self):
    t = TunableIterable(it.count(),
      TunableIterable(it.count()),
    )
    for i, r in enumerate(t):
      self.assertEqual(
        (i, (i,)),
        r
      )
      if i > 10:
        break

  # def test_nested_tunable_iterable_with_choice(self):
  #   t = TunableIterable(it.count(),
  #     TunableChoice(1,2,3),
  #   )
  #   for i, r in enumerate(t):
  #     self.assertEqual(
  #       (i, (i,)),
  #       r
  #     )
  #     if i > 10:
  #       break

  def test_efficiency(self):
    T1 = Tunable(
      *[
          TunableChoice(
            Tunable(
              TunableChoice(a, b)
            ),
            Tunable(
              TunableChoice(a, b)
            ),
          )
          for a in range(2)
          for b in range(2)
      ],
    )
    T1_start = time.perf_counter()
    T1_len = float(len(list(T1)))
    T1_end = time.perf_counter()
    T2 = Tunable(
      *[
          TunableChoice(
            Tunable(
              TunableChoice(a, b, c)
            ),
            Tunable(
              TunableChoice(a, b, c)
            ),
            Tunable(
                TunableChoice(a, b, c)
            ),
          )
          for a in range(3)
          for b in range(2)
          for c in range(2)
      ],
    )
    T2_start = time.perf_counter()
    T2_len = float(len(list(T2)))
    T2_end = time.perf_counter()
    # This complexity was found through trial and error,
    #  I'm actually impressed that it's sqrt
    complexity = lambda n: np.sqrt(n)
    T1_normalized_time = float(T1_end - T1_start) / complexity(T1_len)
    T2_normalized_time = float(T2_end - T2_start) / complexity(T2_len)
    difference = abs(T1_normalized_time - T2_normalized_time)
    print(T1_end - T1_start,
          complexity(T1_len),
          T1_normalized_time)
    print(T2_end - T2_start,
          complexity(T2_len),
          T2_normalized_time)
    assert difference < .01, difference

  def test_tunable_strange_ordering(self):
    self.assertMatchAnyOrder(
        Tunable(dummy,
                1, 2,
          TunableChoice(
            a=3, b=4,
          ),
          TunableChoice(5, 6,),
        ),
        [
          ((1, 2, 5), {'a': 3}),
          ((1, 2, 5), {'b': 4}),
          ((1, 2, 6), {'a': 3}),
          ((1, 2, 6), {'b': 4}),
        ])
