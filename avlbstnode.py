"""
AVL BinarySearchTree Node Class

Nodes to be used in AVLBST. Each node stores data
as a key-value pair. Nodes also store left and right
pointers and their current height in the tree.

J. Knerr
Fall 2018
"""

class AVLBSTNode(object):

  def __init__(self,key,value,height=-1,left=None,right=None):
    """node constructor:key,value,height,left,right"""
    self.key = key
    self.value = value
    self.height = height
    self.left = left
    self.right = right

  def __repr__(self):
    """goal is to be unambiguous"""
    # https://stackoverflow.com/questions/1436703/difference-between-str-and-repr
    return "%s(%s,%s,%d,%s,%s)" % (self.__class__.__name__,
                                   self.key,self.value,
                                   self.height,self.left,self.right)
  def __str__(self):
    """goal is to be readable"""
    # https://stackoverflow.com/questions/1436703/difference-between-str-and-repr
    return "key: %4s,  val: %10s,  height: %3d" % (self.key,
                                                   self.value, 
                                                   self.height)

  # getters and setters
  def getKey(self):    
    """get key from node"""
    return self.key
  def getValue(self):
    """get value from node"""
    return self.value
  def getHeight(self): 
    """get height of node (-1=undef)"""
    return self.height
  def getLeft(self):   
    """get left pointer from node"""
    return self.left
  def getRight(self):  
    """get right pointer from node"""
    return self.right

  def setKey(self,key):
    """change key stored in node"""
    # need when moving nodes around...like remove(key)
    self.key = key
  def setValue(self,value):
    """change value stored in node"""
    self.value = value
  def setHeight(self,height):
    """set height of node"""
    self.height = height
  def setLeft(self,node):
    """set left pointer"""
    self.left = node
  def setRight(self,node):
    """set right pointer"""
    self.right = node

# ---------------------------------------------- #

def main():
  """some simple test code"""

  n1 = AVLBSTNode("A", 356)
  print(n1)
  n2 = AVLBSTNode(5,"hello",3,None,n1)
  print(n2)
  assert(n2.getKey()==5)
  assert(n2.getValue()=="hello")
  assert(n2.getHeight()==3)
  assert(n2.getLeft()==None)
  assert(n2.getRight().getHeight()==-1)

if __name__ == "__main__":
  main()
