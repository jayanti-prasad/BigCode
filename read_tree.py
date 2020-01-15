import os
import sys 
import pickle
from anytree.exporter import DotExporter
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter
from ast_model import Tree 

if __name__ == "__main__":
  
   #with open(sys.argv[1],"rb") as fp:
   #   ast = pickle.load(fp)


   T = Tree(sys.argv[1])

   ast = T.anytree 

   nodes  = [node  for node in PreOrderIter(ast)]
   DotExporter(ast).to_picture("tree.png")
   for n in nodes:
       print(n)
