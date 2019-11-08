import sys
from anytree.exporter import DotExporter
from anytree import PreOrderIter
from big_code_ast_model  import Tree 
from big_code_ast_diff import get_ast_seq 

if __name__ == "__main__":

    T = Tree (sys.argv[1])

    with open(sys.argv[1], "r") as fp:
        code = fp.read()

  
    DotExporter(T.anytree).to_picture("bubble.png")
    
    nodes = [node for node in PreOrderIter(T.anytree)]

    num_lines = len(code.split("\n"))

    ast_seq  = get_ast_seq(1, num_lines, T.anytree)

    code_lines = code.split("\n") 

    for i in range(0, len(code_lines)):
       print(i, code_lines[i]) 

    for seq in ast_seq:
       print(seq)

    for n in nodes:
        print(n)
