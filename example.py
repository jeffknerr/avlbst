"""
example use of avlbst class: python3 example.py

J. Knerr
Fall 2018
"""

import avlbst
from subprocess import call

def printkey(node):
  """function passed to traverseInOrder"""
  # change the print to display whatever you want
  print("key = %d" % node.getKey())

def main():
  # make an empty BST
  bst = avlbst.AVLBST()

  # insert some key-value pairs
  uids = [1611,1819,1320,4276,1797,1558,1000]
  unames = ["lisa","andy","rich","douglas","jeff","cfk","parrish"]
  for i in range(len(uids)):
    key = uids[i]
    val = unames[i]
    bst.insert(key,val)

  # print/show the tree
  print(bst)
  bst.traverseInOrder(printkey)

  # if you have graphviz (dot) and ImageMagick (display) 
  # installed, try this:
  fn = "bst.dot"
  bst.writeDotFile(fn)
  call("dot -Tpng ./%s -O" % fn, shell=True)
  call("display ./%s.png" % fn, shell=True)

main()
