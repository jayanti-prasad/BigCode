from concurrent import futures
from anytree import Node
import bblfsh
import hashlib

def get_hash(tree):
    hash_object = hashlib.md5(str(tree).encode())
    h = hash_object.hexdigest()
    return h

def get_node_properties (tree):
    node_properties  = {'internal_type': None,
           'roles': [],
           'token': "",
           'start_line': tree.start_position.line,
           'end_line': tree.end_position.line }

    if '@type' in tree.get_dict():
        node_properties['internal_type'] = tree.internal_type  

    if '@role' in tree.get_dict():
         try:
             node_properties['roles'] = [bblfsh.role_name(r) for r in tree.roles]
         except:
             pass 

    if node_properties['internal_type']  == 'uast:Identifier':
        node_properties['token'] = tree.get()['Name']

    if node_properties['internal_type']  == 'java:Modifier':
        node_properties['token'] = tree.token

    return node_properties


class Tree:

    def __init__(self, source_file):
        client = bblfsh.BblfshClient("localhost:9432")
        tree = client.parse(source_file).ast
        self.id = 0
        self.nodes = []
        self.nmap = {}
        self.anytree = None
        self.__process__(tree, tree)
        self.__node_mapping__()
        self.anytree = self.__get_any_tree__()
    

    def __process__(self, parent, tree):
 
        node_properties = get_node_properties (tree) 
        node_properties['hash'] = get_hash(node_properties)
        node_properties['parent'] = get_hash(get_node_properties(parent))
        node_properties['id'] =  self.id  
        self.nodes.append(node_properties)
        self.id = self.id + 1
        num_children = len(tree.children)
        for i in range(0, num_children):
             if '@type' in tree.children[i].get_dict():
                 self.__process__(tree, tree.children[i])

    def __node_mapping__(self):
        for n in self.nodes:
            self.nmap[n['hash']] = str(n['id'])

    def __get_any_tree__(self):
        tnodes = []
        for n in self.nodes:
           tnodes.append("x")
        D = {}
        count = 0
        for n in self.nodes:
           if n['id'] == 0:
              parent=None 
           else:
              parent = D[n['parent']]
           tnodes[count] = Node(self.nmap[n['hash']], parent,\
               internal_type=n['internal_type'], roles=n['roles'], token=n['token'],\
               start_line=n['start_line'], end_line=n['end_line'])
           D[n['hash']] = tnodes[count]                
           count = count + 1

        return tnodes[0]
