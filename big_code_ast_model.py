from concurrent import futures
from anytree import Node
import bblfsh
import hashlib

def get_hash(tree):
    hash_object = hashlib.md5(str(tree).encode())
    h = hash_object.hexdigest()
    return h

def get_node_properties (tree):
     D = tree.get_dict()
     node_properties = {}
     node_properties['token'] = "" 
     node_properties['roles'] = []
     if '@type' in tree.get_dict():
         node_properties['internal_type'] =  tree.internal_type
     else:
         node_properties['internal_type'] = None  
     if '@pos' in D:
         node_properties['start_line'] = D['@pos']['start']['line']
         node_properties['start_col'] = D['@pos']['start']['col'] 
         node_properties['end_line'] = D['@pos']['end']['line']
         node_properties['end_col'] = D['@pos']['end']['col'] 
     else:
         node_properties['start_line'] = 0 
         node_properties['start_col'] = 0
         node_properties['end_line'] = 0 
         node_properties['end_col'] = 0
     if '@role' in tree.get_dict():
        try: 
             node_properties['roles'] = [bblfsh.role_name(r) for r in tree.roles]
        except:
             pass 

     if '@token' in tree.get_dict():
         node_properties['token'] = tree.token

     if node_properties['internal_type']  == 'uast:Identifier':
         node_properties['token'] = tree.get()['Name']

     return node_properties


class Tree:

    def __init__(self, source_file):
        client = bblfsh.BblfshClient("localhost:9432")
        tree = client.parse(source_file).ast
        self.id = 0
        self.nodes = []
        self.nmap = {}
        self.visited = [] 
        self.anytree = None
        self.__process__(tree, tree)
        self.__node_mapping__()
        self.anytree = self.__get_any_tree__()
    

    def __process__(self, parent, tree):
        D = tree.get_dict()
        node_properties = get_node_properties (tree) 
        node_properties['hash'] = get_hash(node_properties)
        node_properties['parent'] = get_hash(get_node_properties(parent))
        node_properties['id'] =  self.id  
        if node_properties['hash'] not in self.visited:
           print(node_properties) 
           self.nodes.append(node_properties)
           self.id = self.id + 1
           self.visited.append(node_properties['hash'])
        num_children = len(tree.children)
        for i in range(0, num_children):
            self.__process__(tree, tree.children[i])

    def __node_mapping__(self):
        for n in self.nodes:
            self.nmap[n['hash']] = str(n['id'])

    def __get_any_tree__(self):

        # create the root node 
        root_node = Node (self.nmap[self.nodes[0]['hash']], internal_type=self.nodes[0]['internal_type'],
           roles=self.nodes[0]['roles'], token=self.nodes[0]['token'],
           start_line=self.nodes[0]['start_line'], start_col=self.nodes[0]['start_col'],
           end_line=self.nodes[0]['end_line'], end_col=self.nodes[0]['end_col'])

        anodes = ["x"] * len(self.nodes)
        anodes[0] =  root_node 
        count = 1   
        for n in self.nodes[1:]:
           node_id = self.nmap[n['hash']]
           parent = int(self.nmap[n['parent']])   
           anodes[count] = Node (node_id, anodes[parent], internal_type = n['internal_type'],
           roles=n['roles'], token=n['token'],
           start_line=n['start_line'], start_col = n['start_col'],
           end_line=n['end_line'], end_col = n['end_col'])            
           count = count + 1            
        return root_node
