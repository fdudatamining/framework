from unittest import TestCase

class TestCaseEx(TestCase):
  def assertMatchAnyOrder(self, a, b, c=None):
    a = list(a)
    b = list(b)
    print('Comparing \n%s\n and \n%s' % (repr(a), repr(b)))
    self.assertEqual(len(a), len(b), 'len(%s) != len(%s)' % (repr(a), repr(b)))
    for aa in a:
      if aa not in b:
        self.fail('%s not in %s' % (repr(aa), repr(b)) if c is None else c)
    for bb in b:
      if bb not in a:
        self.fail('%s not in %s' % (repr(bb), repr(a)) if c is None else c)
