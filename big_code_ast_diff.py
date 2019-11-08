from anytree import PreOrderIter

def get_ast_seq(start_line, end_line, ast_tree):

    nodes = [node for node in PreOrderIter(ast_tree)]

    line_map = {}
    for n in nodes:
        if str(n.start_line) not in line_map:
            line_map [str(n.start_line)] = []
        line_map[str(n.start_line)].append(n.internal_type)

    ast_seq = []

    for i in range(start_line, end_line+1):
        try:
           ast_seq.append(str(i-1) +":"+ " ".join(line_map[str(i)]))
        except:
           pass 
    return ast_seq 
