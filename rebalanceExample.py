"""
example showing avl rebalancing: python3 avlexample.py

J. Knerr
Fall 2018
"""

import avlbst
from subprocess import call
from random import randrange, shuffle

def printkeyvals(node):
  """used for traverseInOrder below"""
  # change the print to display whatever you want
  print("key: %s  value: %s" % (str(node.getKey()), 
                                str(node.getValue())))

def main():
  # make an empty BST
  bst = avlbst.AVLBST()

  # insert key-value pairs, show tree rebalancing
  keys = list("ABCDEFGHIJKLMNO")
  for key in keys:
    val = randrange(100)
    print("inserting %s-%d" % (key,val))
    bst.insert(key,val)
    assert(bst.checkInvariants()==True)
    bst.traverseInOrder(printkeyvals)
    # if you have graphviz (dot) and ImageMagick (display) 
    # installed, try these:
    fn = "bst.dot"
    bst.writeDotFile(fn)
    call("dot -Tpng ./%s -O" % fn, shell=True)
    call("display ./%s.png" % fn, shell=True)

main()
