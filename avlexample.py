"""
example showing avl rebalancing: python3 avlexample.py

J. Knerr
Fall 2018
"""

import avlbst
from subprocess import call
from random import randrange

def main():

  # make an empty BST
  bst = avlbst.AVLBST()

  # insert some key-value pairs
  keys = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
  #keys.reverse()
  line = "-"*40
  for key in keys:
    val = randrange(100)
    print("%s\ninserting %s-%d" % (line,key,val))
    bst.insert(key,val)
    # print/show the tree as we build it
    print(bst)
    bst.printInOrder()
    fn = "bst.dot"
    bst.writeDotFile(fn)
    # if you have graphviz (dot) and ImageMagick (display) 
    # installed, try these:
    call("dot -Tpng ./%s -O" % fn, shell=True)
    call("display ./%s.png" % fn, shell=True)

main()
