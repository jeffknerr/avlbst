import unittest
from avlbst import *
from random import randrange, choice, shuffle

class TestAVLBSTMethods(unittest.TestCase):

  def setUp(self):
    """create empty avlbst"""
    self.bst = AVLBST()
    self.assertEqual(self.bst.getSize(), 0)
    self.keys = list("MFTBIPXHADGLQUYZ")
    self.length = len(self.keys)
    self.values = []
    for i in range(len(self.keys)):
      self.values.append(randrange(100))

  def test_empty(self):
    self.assertEqual(self.bst.getSize(), 0)
    self.assertEqual(self.bst.isEmpty(), True)
    self.assertEqual(self.bst.checkInvariants(), True)

  def test_inserts(self):
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
      self.assertEqual(self.bst.checkInvariants(), True)
    self.assertEqual(self.bst.getSize(), self.length)
    self.assertEqual(self.bst.isEmpty(), False)

  def test_removes(self):
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    length = self.length
    for i in range(self.length):
      key = choice(self.keys)
      self.bst.remove(key)
      self.assertEqual(self.bst.checkInvariants(), True)
      length -= 1
      self.assertEqual(self.bst.getSize(), length)
      self.keys.remove(key)
    self.assertEqual(self.bst.isEmpty(), True)

  def test_differentOrder(self):
    shuffle(self.keys)
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
      self.assertEqual(self.bst.checkInvariants(), True)
    self.assertEqual(self.bst.getSize(), self.length)
    self.assertEqual(self.bst.isEmpty(), False)
    shuffle(self.keys)
    length = self.length
    for i in range(self.length):
      key = choice(self.keys)
      self.bst.remove(key)
      self.assertEqual(self.bst.checkInvariants(), True)
      length -= 1
      self.assertEqual(self.bst.getSize(), length)
      self.keys.remove(key)
    self.assertEqual(self.bst.isEmpty(), True)

  def test_minmax(self):
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    self.assertEqual(self.bst.findMax().getKey(), max(self.keys))
    self.assertEqual(self.bst.findMin().getKey(), min(self.keys))
    imax = self.keys.index(max(self.keys))
    self.assertEqual(self.bst.findMax().getValue(), self.values[imax])
    imin = self.keys.index(min(self.keys))
    self.assertEqual(self.bst.findMin().getValue(), self.values[imin])

####################################################

if __name__ == '__main__':
  unittest.main()
