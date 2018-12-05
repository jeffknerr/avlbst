"""
AVL BinarySearchTree Class

AVL (Adelson-Velsky and Landis) Binary Search Tree

J. Knerr
Fall 2018
"""

from avlbstnode import *
import sys

class AVLBST(object):

  def __init__(self):
    """avlbst constructor: creates initially empty binary search tree"""
    self.size = 0
    self.root = None

  def __repr__(self):
    return "%s()" % (self.__class__.__name__)
  def __str__(self):
    return "Size: %d, Root: %s" % (self.size, self.root)

  def getSize(self):    
    """return size of tree"""
    return self.size
  def __len__(self):
    """return size of tree"""
    return self.size
  def isEmpty(self):  
    """return True if tree is empty, False if not"""
    return self.size == 0

  def insert(self, key, value):
    """add a new node (key-value pair) to the tree"""
    if self.size == 0:
      newnode = AVLBSTNode(key, value, 0)
      self.root = newnode
      self.size += 1
    else:
      self.root = self._insertInSubtree(self.root, key, value)

  def _insertInSubtree(self, curr, key, value):
    """private helper function: add new node to correct spot in subtree"""
    ckey = curr.getKey()
    if key < ckey:
      # go left
      if curr.getLeft() == None:
        # insert here
        newnode = AVLBSTNode(key,value,0)
        curr.setLeft(newnode)
        self.size += 1
      else:
        curr.setLeft(self._insertInSubtree(curr.getLeft(), key, value))
      self._recalcHeight(curr)
      curr = self._rebalance(curr)
      return curr
    elif key > ckey:
      # go right
      if curr.getRight() == None:
        # insert here
        newnode = AVLBSTNode(key,value,0)
        curr.setRight(newnode)
        self.size += 1
      else:
        curr.setRight(self._insertInSubtree(curr.getRight(), key, value))
      self._recalcHeight(curr)
      curr = self._rebalance(curr)
      return curr
    else:
      print("insert() error: trying to insert duplicate key (%s)" % str(key))
      return curr

  def remove(self, key):
    """look for key in BST, remove node if found"""
    self.root = self._removeFromSubtree(self.root, key)

  def _removeFromSubtree(self, curr, key):
    """private helper function to remove node with key (if found)"""
    if curr == None:
      print("remove() error: no such key (%s) to remove." % str(key))
      return curr
    elif key < curr.getKey():
      curr.setLeft(self._removeFromSubtree(curr.getLeft(), key))
      self._recalcHeight(curr)
      curr = self._rebalance(curr)
      return curr
    elif key > curr.getKey():
      curr.setRight(self._removeFromSubtree(curr.getRight(), key))
      self._recalcHeight(curr)
      curr = self._rebalance(curr)
      return curr
    else:
      # found key....so need to delete this curr node
      CL = curr.getLeft()
      CR = curr.getRight()
      if CL==None and CR==None:
        # leaf node...easy
        self.size -= 1
        return None
      elif CL==None:
        # promote the right node
        self.size -= 1
        return CR
      elif CR==None:
        # promote the left node
        self.size -= 1
        return CL
      else:
        # find min of right subtree, swap and remove it
        minright = self._getMinInSubtree(CR)
        curr.setKey(minright.getKey())
        curr.setValue(minright.getValue())
        curr.setRight(self._removeFromSubtree(CR,minright.getKey()))
        self._recalcHeight(curr)
        curr = self._rebalance(curr)
        return curr

  def _getMinInSubtree(self, curr):
    """get left-most node (should have smallest key)"""
    # since it's a BST, we want the left-most node
    # (assumes BST is correct!)
    if curr.getLeft()==None:
      return curr
    else:
      return self._getMinInSubtree(curr.getLeft())

  def _getMaxInSubtree(self, curr):
    """get right-most node (should have largest key)"""
    # since it's a BST, we want the right-most node
    # (assumes BST is correct!)
    if curr.getRight()==None:
      return curr
    else:
      return self._getMaxInSubtree(curr.getRight())

  # AVL rebalance based on info from the wikipedia page:
  # https://en.wikipedia.org/wiki/AVL_tree
  # the 4 cases:
  # RR: Z is right child of X, Z is right-heavy
  # LL: Z is left  child of X, Z is left-heavy
  # RL: Z is right child of X, Z is left-heavy
  # LR: Z is left  child of X, Z is right-heavy
  # first two are handled by "simple" single rotations (left, right)
  # next two are handled by double rotations (rightLeft, leftRight)

  def _leftRotate(self, X, Z):
    """left-rotate, so Z becomes root, X becomes left-child of Z"""
    # this is the RR case above
    t23 = Z.getLeft()   # see wikipedia page for X,Z,t23
    X.setRight(t23)
    Z.setLeft(X)
    self._recalcHeight(X)
    return Z

  def _rightRotate(self, X, Z):
    """right-rotate, so Z becomes root, X becomes right-child of Z"""
    # this is the LL case above
    t23 = Z.getRight()
    X.setLeft(t23)
    Z.setRight(X)
    self._recalcHeight(X)
    return Z

  def _rightLeftRotate(self, X, Z):
    """double rotate: first right, then left"""
    # this is the RL case above
    Y = Z.getLeft()                  #   X           Y
    self._rightRotate(Z, Y)          #     Z   --> X   Z
    X.setRight(Y)                    #   Y
    self._leftRotate(X, Y)
    self._recalcHeight(Y)
    self._recalcHeight(X)
    self._recalcHeight(Z)
    return Y

  def _leftRightRotate(self, X, Z):
    """double rotate: first left, then right"""
    # this is the LR case above
    Y = Z.getRight()                 #   X          Y
    self._leftRotate(Z, Y)           # Z     -->  Z   X
    X.setLeft(Y)                     #   Y
    self._rightRotate(X, Y)
    self._recalcHeight(Y)
    self._recalcHeight(X)
    self._recalcHeight(Z)
    return Y

  def _getSubTreeHeight(self, curr):
    """given a node, get height of node's subtree"""
    if curr == None:
      return 0
    else:
      return curr.getHeight() + 1

  def _rebalance(self, curr):
    """given a node in the tree, check if we need to rebalance"""
    # based on code from https://www.cs.swarthmore.edu/courses/CS35/F18/labs/07
    LSH = self._getSubTreeHeight(curr.getLeft())   # left subtree height
    RSH = self._getSubTreeHeight(curr.getRight())  # right subtree height
    delta = RSH - LSH
    if (delta < -1):
      # left height too big
      LLH = self._getSubTreeHeight(curr.getLeft().getLeft())  # left-left-height
      LRH = self._getSubTreeHeight(curr.getLeft().getRight()) # left-right-height
      if LLH < LRH:
        curr = self._leftRightRotate(curr, curr.getLeft())
      else:
        curr = self._rightRotate(curr, curr.getLeft())
    elif (delta > 1):
      # right height too big
      RRH = self._getSubTreeHeight(curr.getRight().getRight()) # right-right-height
      RLH = self._getSubTreeHeight(curr.getRight().getLeft())  # right-left-height
      if RLH > RRH:
        curr = self._rightLeftRotate(curr, curr.getRight())
      else:
        curr = self._leftRotate(curr, curr.getRight())
    return curr

  def findMax(self):
    """find and return node with largest key in tree"""
    return self._findMaxInSubtree(self.root)

  def findMin(self):
    """find and return node with smallest key in tree"""
    return self._findMinInSubtree(self.root)

  def _findMaxInSubtree(self, curr):
    """traverse the whole subtree, return node with largest key"""
    if curr == None:
      return None
    else:
      ckey = curr.getKey()
      Lmax = self._findMaxInSubtree(curr.getLeft())
      Rmax = self._findMaxInSubtree(curr.getRight())
      if Lmax==None and Rmax==None:
        return curr
      elif Lmax==None:
        if ckey > Rmax.getKey():
          return curr
        else:
          return Rmax
      elif Rmax==None:
        if ckey > Lmax.getKey():
          return curr
        else:
          return Lmax
      else:
        rkey = Rmax.getKey()
        lkey = Lmax.getKey()
        if ckey > rkey and ckey > lkey:
          return curr
        elif rkey > ckey and rkey > lkey:
          return Rmax
        else:
          return Lmax

  def _findMinInSubtree(self, curr):
    """traverse the whole subtree, return node with smallest key"""
    if curr == None:
      return None
    else:
      ckey = curr.getKey()
      Lmin = self._findMinInSubtree(curr.getLeft())
      Rmin = self._findMinInSubtree(curr.getRight())
      if Lmin==None and Rmin==None:
        return curr
      elif Lmin==None:
        if ckey < Rmin.getKey():
          return curr
        else:
          return Rmin
      elif Rmin==None:
        if ckey < Lmin.getKey():
          return curr
        else:
          return Lmin
      else:
        rkey = Rmin.getKey()
        lkey = Lmin.getKey()
        if ckey < rkey and ckey < lkey:
          return curr
        elif rkey < ckey and rkey < lkey:
          return Rmin
        else:
          return Lmin

  def _countNodes(self, curr):
    """return number of nodes from here down"""
    if curr == None:
      return 0
    else:
      return self._countNodes(curr.getLeft()) + self._countNodes(curr.getRight()) + 1

  def _checkKeys(self, curr):
    """check that keys are all in order for BST"""
    if curr == None:
      return True
    else:
      minRight = self._findMinInSubtree(curr.getRight())
      maxLeft = self._findMaxInSubtree(curr.getLeft())
      if minRight==None and maxLeft==None:
        return True
      elif minRight==None:
        return curr.getKey() > maxLeft.getKey()
      elif maxLeft==None:
        return curr.getKey() < minRight.getKey()
      else:
        return maxLeft.getKey() < curr.getKey() and curr.getKey() < minRight.getKey()

  def checkInvariants(self):
    """check the BST to make sure it's valid"""
    # based on code from https://www.cs.swarthmore.edu/courses/CS35/F18/labs/07
    # make sure size is correct
    count = self._countNodes(self.root)
    if count != self.size:
      print("BST size incorrect!!!")
      return False
    # make sure max of left < key < min of right for all nodes.
    # warning...I think this is an O(nlog(n)) algorithm, since for every node,
    # you need to visit all nodes below (to find the min/max).
    # for testing when not valid: 
    # self.root.setKey("Z")
    if not self._checkKeys(self.root):
      print("BST keys out of order!!!")
      return False
    # all good if we get here...
    return True

  def traverseInOrder(self, f):
    """in-order traversal: apply function f(node) to each node"""
    if callable(f):
      self._traverseInOrder(self.root, f)
    else:
      print("traverseInOrder(f) error: f must be a callable function")

  def _traverseInOrder(self, curr, f):
    """private helper function to apply f during in-order traversal"""
    if curr == None:
      return
    else:
      self._traverseInOrder(curr.getLeft(), f)
      f(curr)
      self._traverseInOrder(curr.getRight(), f)

  def traversePreOrder(self, f):
    """pre-order traversal: apply function f(node) to each node"""
    if callable(f):
      self._traversePreOrder(self.root, f)
    else:
      print("traversePreOrder(f) error: f must be a callable function")

  def _traversePreOrder(self, curr, f):
    """private helper function to apply f during pre-order traversal"""
    if curr == None:
      return
    else:
      f(curr)
      self._traversePreOrder(curr.getLeft(), f)
      self._traversePreOrder(curr.getRight(), f)

  def traversePostOrder(self, f):
    """post-order traversal: apply function f(node) to each node"""
    if callable(f):
      self._traversePostOrder(self.root, f)
    else:
      print("traversePostOrder(f) error: f must be a callable function")

  def _traversePostOrder(self, curr, f):
    """private helper function to apply f during post-order traversal"""
    if curr == None:
      return
    else:
      self._traversePostOrder(curr.getLeft(), f)
      self._traversePostOrder(curr.getRight(), f)
      f(curr)

  def _recalcHeight(self, curr):
    """calculate/set height of given node"""
    if curr.getLeft() == None:
      lefth = -1
    else:
      lefth = curr.getLeft().getHeight()
    if curr.getRight() == None:
      righth = -1
    else:
      righth = curr.getRight().getHeight()
    curr.setHeight(max(lefth,righth) + 1)

# https://eli.thegreenplace.net/2009/11/23/visualizing-binary-trees-with-graphviz

  def writeDotFile(self, filename):
    """make xdot file, so we can actually *see* the tree"""
    nullcount = 0
    try:
      ofl = open(filename,"w")
    except:
      print("writeDotFile() unable to open file (%s)...exiting now." % filename)
      sys.exit(1)
    ofl.write("digraph BST {\n")
    ofl.write("   node [fontname=\"Arial\"];\n")
    if self.root == None:
      ofl.write("\n")
    elif self.root.getLeft()==None and self.root.getRight()==None:
      ofl.write("    %s;\n" % (self.root.getDesc()))
    else:
      self._helperDot(self.root, ofl, nullcount)
    ofl.write("}\n")
    ofl.close()

  def _helperDot(self, curr, ofl, nullcount):
    """private helper function for writing out xdot file"""
    if curr.getLeft() != None:
      ofl.write("   %s -> %s ;\n" % (curr.getDesc(),curr.getLeft().getDesc()))
      nullcount = self._helperDot(curr.getLeft(), ofl, nullcount)
    else:
      nullcount += 1
      self._nullDot(curr.getDesc(), nullcount, ofl)
    if curr.getRight() != None:
      ofl.write("   %s -> %s ;\n" % (curr.getDesc(),curr.getRight().getDesc()))
      nullcount = self._helperDot(curr.getRight(), ofl, nullcount)
    else:
      nullcount += 1
      self._nullDot(curr.getDesc(), nullcount, ofl)
    return nullcount

  def _nullDot(self, description, nullcount, ofl):
    """private helper function to write null nodes"""
    ofl.write("   null%d [shape=point];\n" % nullcount)
    ofl.write("   %s -> null%d;\n" % (description,nullcount))

# ---------------------------------------------- #

from random import randrange, choice
from subprocess import call

def display(fn):
  """turn a dot file into a png and display it"""
  call("dot -Tpng ./%s -O" % fn, shell=True)
  call("display ./%s.png" % fn, shell=True)

def nodeprint(node):
  """given a node, print the node"""
  print(node)

def main():
  """some simple test code"""

  # make BST
  bst = AVLBST()
  assert(bst.getSize()==0)
  assert(bst.isEmpty()==True)

  # insert tests
  bst.insert("C",5)
  keys = list("ABCDEFG")
  length = len(keys)
  val = 10
  for key in keys:
    bst.insert(key,val)
    val += 10
  assert(len(bst)==length)
  assert(bst.checkInvariants() == True)
  assert(bst.isEmpty()==False)
  bst.traverseInOrder(nodeprint)
  fn = "bst.dot"
  bst.writeDotFile(fn)
  display(fn)
  
if __name__ == "__main__":
  main()
