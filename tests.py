import unittest, io
from avlbst import *
from random import randrange, choice, shuffle

class TestAVLBSTMethods(unittest.TestCase):

  def setUp(self):
    """create empty avlbst"""
    self.bst = AVLBST()
    self.assertEqual(self.bst.getSize(), 0)
    self.keys = list("ABCDEFGHIJKLMNOPQ")
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
    self.assertEqual(self.bst.getSize(), len(self.keys))
    self.assertEqual(self.bst.isEmpty(), False)

  def test_removes(self):
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    length = len(self.keys)
    for i in range(length):
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
    self.assertEqual(self.bst.getSize(), len(self.keys))
    self.assertEqual(self.bst.isEmpty(), False)
    shuffle(self.keys)
    length = len(self.keys)
    for i in range(length):
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

  def test_insertduplicate(self):
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    output = io.StringIO()
    sys.stdout = output
    self.bst.insert(k,v)
    emsg = "insert() error: trying to insert duplicate key (%s)" % str(k)
    self.assertEqual(output.getvalue().strip('\n'), emsg)
    self.assertEqual(self.bst.checkInvariants(), True)
    self.assertEqual(self.bst.getSize(), len(self.keys))

  def test_removenonexistent(self):
    output = io.StringIO()
    sys.stdout = output
    key = "supercalifragilistic"
    self.bst.remove(key)
    emsg = "remove() error: no such key (%s) to remove." % str(key)
    self.assertEqual(output.getvalue().strip('\n'), emsg)
    self.assertEqual(self.bst.checkInvariants(), True)
    self.assertEqual(self.bst.getSize(), 0)

  def test_traversals(self):
    globalL = []
    def getnodekey(node):
      """key from given node"""
      globalL.append(node.getKey())
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    # in order test
    self.bst.traverseInOrder(getnodekey)
    lstr = "".join(globalL)
    self.keys.sort()
    kstr = "".join(self.keys)
    self.assertEqual(lstr,kstr)
    # pre order test
    globalL.clear()
    self.bst.traversePreOrder(getnodekey)
    lstr = "".join(globalL)
    prestr = "HDBACFEGLJIKNMPOQ"
    self.assertEqual(lstr,prestr)
    # post order test
    globalL.clear()
    self.bst.traversePostOrder(getnodekey)
    lstr = "".join(globalL)
    poststr = "ACBEGFDIKJMOQPNLH"
    self.assertEqual(lstr,poststr)

  def test_contains(self):
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    for i in range(len(self.keys)):
      k = self.keys[i]
      self.assertEqual(self.bst.contains(k), True)
    self.assertEqual(self.bst.contains("".join(self.keys)), False)

  def test_update(self):
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    for i in range(len(self.keys)):
      k = self.keys[i]
      self.bst.update(k,"hello")
    self.assertEqual(self.bst.checkInvariants(), True)
    self.assertEqual(self.bst.getSize(), len(self.keys))
    output = io.StringIO()
    sys.stdout = output
    key = "supercalifragilistic"
    self.bst.update(key,"hello")
    emsg = "update() error: no such node with key (%s) to update." % str(key)
    self.assertEqual(output.getvalue().strip('\n'), emsg)
    self.assertEqual(self.bst.checkInvariants(), True)
    self.assertEqual(self.bst.getSize(), len(self.keys))

  def test_get(self):
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    for i in range(len(self.keys)):
      k = self.keys[i]
      self.assertEqual(self.bst.get(k), self.values[i])
    output = io.StringIO()
    sys.stdout = output
    key = "supercalifragilistic"
    result = self.bst.get(key)
    self.assertEqual(result, None)
    emsg = "get() error: no such node with key (%s) to get." % str(key)
    self.assertEqual(output.getvalue().strip('\n'), emsg)
    self.assertEqual(self.bst.checkInvariants(), True)
    self.assertEqual(self.bst.getSize(), len(self.keys))

  def test_getkeys(self):
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    klist = self.bst.getKeys()
    self.assertEqual(len(klist), len(self.keys))
    for i in range(len(self.keys)):
      self.assertEqual(klist[i], self.keys[i])
    self.assertEqual(self.bst.checkInvariants(), True)
    self.assertEqual(len(self.bst), len(self.keys))

  def test_getitems(self):
    for i in range(len(self.keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    ilist = self.bst.getItems()  # item list of (key,val) tuples
    self.assertEqual(len(ilist), len(self.keys))
    for i in range(len(self.keys)):
      self.assertEqual(ilist[i][0], self.keys[i])
      self.assertEqual(ilist[i][1], self.values[i])
    self.assertEqual(self.bst.checkInvariants(), True)
    self.assertEqual(len(self.bst), len(self.keys))

  def test_levelordertraversal(self):
    keys = self.keys[0:7]  # just A->G
    for i in range(len(keys)):
      k = self.keys[i]
      v = self.values[i]
      self.bst.insert(k,v)
    ilist = self.bst.traverseLevelOrder()  # item list of (key,val) tuples
    self.assertEqual(len(ilist), len(keys))
    levelorder = list("DBFACEG")
    for i in range(len(keys)):
      self.assertEqual(ilist[i][0], levelorder[i])
    self.assertEqual(self.bst.checkInvariants(), True)
    self.assertEqual(len(self.bst), len(keys))

####################################################

if __name__ == '__main__':
  unittest.main()
