from framework.util import args
from unittest import TestCase

class TestArgs(TestCase):
  def test_nargs(self):
    self.assertEqual(args.nargs(['test']), {}, 'Empty')
    self.assertEqual(args.nargs(['test'], test=None), {}, 'Empty overload')
    self.assertEqual(args.nargs(['test'], test=1), {'test': 1}, 'Set arg')
    self.assertEqual(args.nargs(['test'], test1=2), {}, 'Set unrelated arg')
