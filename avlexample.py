"""
example showing avl rebalancing: python3 avlexample.py

J. Knerr
Fall 2018
"""

import avlbst
from subprocess import call
from random import randrange, shuffle

def main():

  # make an empty BST
  bst = avlbst.AVLBST()

  # insert some key-value pairs
  keys = list("ABCDEFGHIJKLMNO")
  for key in keys:
    val = randrange(100)
    print("inserting %s-%d" % (key,val))
    bst.insert(key,val)
    assert(bst.checkInvariants()==True)
    bst.printInOrder()
    fn = "bst.dot"
    bst.writeDotFile(fn)
    # if you have graphviz (dot) and ImageMagick (display) 
    # installed, try these:
    call("dot -Tpng ./%s -O" % fn, shell=True)
    call("display ./%s.png" % fn, shell=True)

main()
