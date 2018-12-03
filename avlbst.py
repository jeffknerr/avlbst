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
 
  # based on info from the wikipedia page:
  # https://en.wikipedia.org/wiki/AVL_tree
  # the 4 cases:
  # RR: Z is right child of X, Z is right-heavy
  # LL: Z is left child of X, Z is left-heavy
  # RL: Z is right child of X, Z is left-heavy
  # LR: Z is left child of X, Z is right-heavy
  # first two are handled by "simple" single rotations
  # next two are handled by double rotations

  def _leftRotate(self, X, Z):
    """left-rotate, so Z becomes root, X becomes child of Z"""
    t23 = Z.getLeft()
    X.setRight(t23)
    Z.setLeft(X)
    # need to recalcHeights???
    self._recalcHeight(X)
    return Z

  def _rightRotate(self, X, Z):
    """right-rotate, so Z becomes root, X becomes child of Z"""
    t23 = Z.getRight()
    X.setLeft(t23)
    Z.setRight(X)
    # need to recalcHeights???
    self._recalcHeight(X)
    return Z
#   if X.getKey() == self.root.getKey():
#     # new root node!!!!
#     self.root = Z

  def _rightLeftRotate(self, X, Z):
    """double rotate: first right, then left"""
    Y = Z.getLeft()
    self._rightRotate(Z, Y)
    X.setRight(Y)
    self._leftRotate(X, Y)
    # need to recalcHeights???
    self._recalcHeight(Y)
    self._recalcHeight(X)
    self._recalcHeight(Z)
    return Y

  def _leftRightRotate(self, X, Z):
    """double rotate: first left, then right"""
    Y = Z.getRight()
    self._leftRotate(Z, Y)
    X.setLeft(Y)
    self._rightRotate(X, Y)
    # need to recalcHeights???
    self._recalcHeight(Y)
    self._recalcHeight(X)
    self._recalcHeight(Z)
    return Y

  def _rebalance(self, curr):
    """given a node in the tree, check if we need to rebalance"""
    # based on code from https://www.cs.swarthmore.edu/courses/CS35/F18/labs/07
    LSH = self._getSubTreeHeight(curr.getLeft())   # left subtree height
    RSH = self._getSubTreeHeight(curr.getRight())  # right subtree height
    delta = RSH - LSH
    print("delta: %d" % (delta))
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
      print("RRH: %d    RLH: %d" % (RRH,RLH))
      if RLH > RRH:
        print("calling RLrotate")
        curr = self._rightLeftRotate(curr, curr.getRight())
      else:
        print("calling Leftrotate on %s-%s" % (curr.getKey(),curr.getRight().getKey()))
        print(curr)
        print(curr.getRight())
        curr = self._leftRotate(curr, curr.getRight())
        print(curr)
    return curr

  def _getSubTreeHeight(self, curr):
    """given a node, get height of node's subtree"""
    if curr == None:
      return 0
    else:
      return curr.getHeight() + 1

  def remove(self, key):
    """look for key in BST, remove node if found"""
    self.root = self._removeFromSubtree(self.root, key)

  def _removeFromSubtree(self, curr, key):
    """private helper function to remove node with key (if found)"""
    if curr == None:
      print("no such key (%s)...remove(key) call" % str(key))
      return curr
    elif key < curr.getKey():
      curr.setLeft(self._removeFromSubtree(curr.getLeft(), key))
      self._recalcHeight(curr)
      return curr
    elif key > curr.getKey():
      curr.setRight(self._removeFromSubtree(curr.getRight(), key))
      self._recalcHeight(curr)
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
        minright = self.getMinInSubtree(CR)
        curr.setKey(minright.getKey())
        curr.setValue(minright.getValue())
        curr.setRight(self._removeFromSubtree(CR,minright.getKey()))
        self._recalcHeight(curr)
        return curr

  def getMinInSubtree(self, curr):
    """get node in subtree with smallest key"""
    # since it's a BST, we want the left-most node
    # (assumes BST is correct!)
    if curr.getLeft()==None:
      return curr
    else:
      return self.getMinInSubtree(curr.getLeft())

  def getMaxInSubtree(self, curr):
    """get node in subtree with largest key"""
    # since it's a BST, we want the right-most node
    # (assumes BST is correct!)
    if curr.getRight()==None:
      return curr
    else:
      return self.getMaxInSubtree(curr.getRight())

  def findMax(self):
    """find and return largest node/key in tree"""
    return self._findMaxInSubtree(self.root)

  def findMin(self):
    """find and return largest node/key in tree"""
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

  def printInOrder(self):
    """in-order traversal...print each node as visited"""
    self._printInOrder(self.root)

  def _printInOrder(self, curr):
    """private helper function to do in-order traversal"""
    if curr == None:
      return
    else:
      self._printInOrder(curr.getLeft())
      print(curr)
      self._printInOrder(curr.getRight())

  def printPostOrder(self):
    """post-order traversal...print each node as visited"""
    self._printPostOrder(self.root)

  def _printPostOrder(self, curr):
    """private helper function to do post-order traversal"""
    if curr == None:
      return
    else:
      self._printPostOrder(curr.getLeft())
      self._printPostOrder(curr.getRight())
      print(curr)

  def printPreOrder(self):
    """pre-order traversal...print each node as visited"""
    self._printPreOrder(self.root)

  def _printPreOrder(self, curr):
    """private helper function to do pre-order traversal"""
    if curr == None:
      return
    else:
      print(curr)
      self._printPreOrder(curr.getLeft())
      self._printPreOrder(curr.getRight())

  def _recalcHeight(self,curr):
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

  def insert(self,key,value):
    """add a new node to the tree"""
    if self.size == 0:
      newnode = AVLBSTNode(key,value,0)
      self.root = newnode
      self.size += 1
    else:
      self.root = self._insertInSubtree(self.root,key,value)

  def _insertInSubtree(self,curr,key,value):
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
        curr.setLeft(self._insertInSubtree(curr.getLeft(),key,value))
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
        curr.setRight(self._insertInSubtree(curr.getRight(),key,value))
      self._recalcHeight(curr)
      curr = self._rebalance(curr)
      return curr
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

def main():
  """some simple test code"""

  # make BST
  bst = AVLBST()
  print(bst)
  assert(bst.getSize()==0)
  assert(bst.isEmpty()==True)

  # insert tests
  #ABCDEFGHIJKLMNOPQRSTUVWXYZ
  keys = list("MFTBIPXH")
  length = len(keys)
  for k in keys:
    v = randrange(101)
    bst.insert(k,v)
  assert(len(bst)==length)
  assert(bst.checkInvariants() == True)
  assert(bst.isEmpty()==False)
  print(bst)
  bst.printInOrder()
  #bst.printPreOrder()
  #bst.printPostOrder()
  fn = "bst.dot"
  bst.writeDotFile(fn)
  display(fn)
  
  # remove tests
  print("testing remove...")
  bst.remove("F")
  length -= 1
  bst.printInOrder()
  assert(len(bst)==length)
  assert(bst.checkInvariants() == True)

  # min/max tests
  minLetter = min(keys)
  maxLetter = max(keys)
  assert(bst.findMax().getKey()==maxLetter)
  assert(bst.findMin().getKey()==minLetter)

  # more insert tests
  morekeys = list("ADGLQUYZ")
  for k in morekeys:
    v = randrange(101)
    print("adding %s-%d" % (k,v))
    bst.insert(k,v)
  bst.writeDotFile(fn)
  display(fn)
  length += len(morekeys)
  assert(len(bst)==length)
  assert(bst.checkInvariants() == True)
  assert(bst.isEmpty()==False)

if __name__ == "__main__":
  main()
