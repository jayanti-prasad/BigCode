import sys
from anytree.exporter import DotExporter
from anytree import PreOrderIter
from bblfsh_anytree_model  import Tree 


if __name__ == "__main__":

    T = Tree (sys.argv[1])

    DotExporter(T.anytree).to_picture("bubble.png")
    
    nodes = [node for node in PreOrderIter(T.anytree)]
 
    for n in nodes:
        print(n)
