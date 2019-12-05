import os
import sys 
import pickle
from anytree.exporter import DotExporter
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter

if __name__ == "__main__":
  
   with open(sys.argv[1],"rb") as fp:
      ast = pickle.load(fp)
   nodes  = [node  for node in PreOrderIter(ast)]
   DotExporter(ast).to_picture("tree.png")
     for n in nodes:
       print(n)
