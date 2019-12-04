import sys
from ast_model import Tree 
from anytree import Node
from anytree import PreOrderIter

class AstDiff:
    def __init__(self, code, ast, cfg=None):
        self.cfg = cfg
        self.code_lines  = [""] + code.split("\n")
        self.ast = ast
        self.line_map = {} 
        self.__ast_line_map__()


    def __ast_line_map__(self ):

        nodes = [node for node in PreOrderIter(self.ast.anytree)]

        for n in nodes:
            if str(n.start_line) not in self.line_map:
               self.line_map [str(n.start_line)] = []
 
            self.line_map[str(n.start_line)].append(n.internal_type)


    def get_ast_seq(self, start_line, end_line):

        code_block = ""
        ast_block = ""

        for i in range(start_line, end_line):
            if i < len(self.code_lines): 
                code_block = code_block + "\n" + str(i) + ":" +  self.code_lines[i] 
            if str(i) in self.line_map :
                ast_block = ast_block + "\n" + str(i) + ":" +" ".join(self.line_map [str(i)])  
        return code_block, ast_block 
 



if __name__ == "__main__":

     source_file = sys.argv[1]

     with open(source_file,'r') as fp:
         code = fp.read()
     
     T = Tree(source_file)

     D = AstDiff(code, T)  

     code, ast = D.get_ast_seq(1, 5)

     print("code\n", code)
     print("ast\n", ast)


    
