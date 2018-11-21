"""
AVL BinarySearchTree Class

AVL (Adelson-Velsky and Landis) Binary Search Tree

J. Knerr
Fall 2018
"""

from avlbstnode import *

class AVLBST(object):

  def __init__(self):
    """avlbst constructor: creates initially empty tree"""
    self.size = 0
    self.root = None

  def __repr__(self):
    return "%s()" % (self.__class__.__name__)
  def __str__(self):
    return "Size: %d, Root: %s" % (self.size, self.root)

  def getSize(self):    
    """get size of tree"""
    return self.size
  def __len__(self):
    return self.size
  def isEmpty(self):  
    """query tree to see if empty or not"""
    return self.size == 0

  def insert(self,key,value):
    """add a new node to the tree"""
    if self.size == 0:
      newnode = AVLBSTNode(key,value,0)
      self.root = newnode
      self.size += 1
    else:
      self._insertInSubtree(self.root,key,value)

  def _insertInSubtree(self,curr,key,value):
    """private helper function: add new node to correct spot in subtree"""
    ckey = curr.getKey()
    if key < ckey:
      # go left
      if curr.getLeft() == None:
        # insert here
        newnode = AVLBSTNode(key,value)
        curr.setLeft(newnode)
        self.size += 1
      else:
        self._insertInSubtree(curr.getLeft(),key,value)
    elif key > ckey:
      # go right
      if curr.getRight() == None:
        # insert here
        newnode = AVLBSTNode(key,value)
        curr.setRight(newnode)
        self.size += 1
      else:
        self._insertInSubtree(curr.getRight(),key,value)
    else:
      print("Error...duplicate key: %s" % str(key))

  def writeDotFile(self, filename):
    """make a xdot file, so we can actually *see* the tree"""
    # https://eli.thegreenplace.net/2009/11/23/visualizing-binary-trees-with-graphviz
    nullcount = 0
    ofl = open(filename,"w")
    ofl.write("digraph BST {\n")
    ofl.write("   node [fontname=\"Arial\"];\n")
    if self.root == None:
      ofl.write("\n")
    elif self.root.getLeft()==None and self.root.getRight()==None:
      ofl.write("    %s;\n" % (str(self.root.getKey())))
    else:
      self._helperDot(self.root, ofl, nullcount)
    ofl.write("}\n")
    ofl.close()

  def _helperDot(self, curr, ofl, nullcount):
    """private helper function for writing out xdot file"""
    if curr.getLeft() != None:
      ofl.write("   %s -> %s ;\n" % (str(curr.getKey()),
                                     str(curr.getLeft().getKey())))
      nullcount = self._helperDot(curr.getLeft(), ofl, nullcount)
    else:
      nullcount += 1
      self._nullDot(curr.getKey(), nullcount, ofl)
    if curr.getRight() != None:
      ofl.write("   %s -> %s ;\n" % (str(curr.getKey()),
                                     str(curr.getRight().getKey())))
      nullcount = self._helperDot(curr.getRight(), ofl, nullcount)
    else:
      nullcount += 1
      self._nullDot(curr.getKey(), nullcount, ofl)
    return nullcount

  def _nullDot(self, key, nullcount, ofl):
    """private helper function to write null nodes"""
    ofl.write("   null%d [shape=point];\n" % nullcount)
    ofl.write("   %s -> null%d;\n" % (key,nullcount))

# ---------------------------------------------- #

from random import randrange, choice

def main():
  """some simple test code"""

  #ABCDEFGHIJKLMNOPQRSTUVWXYZ
  keys = list("MFTBIPX")
  bst = AVLBST()
  print(bst)
  assert(bst.getSize()==0)
  assert(bst.isEmpty()==True)
  for k in keys:
    v = randrange(101)
    bst.insert(k,v)
  print(bst)
  assert(len(bst)==len(keys))
  bst.writeDotFile("bst.dot")

if __name__ == "__main__":
  main()
