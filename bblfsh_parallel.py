from concurrent import futures
import bblfsh
import sys
from joblib import Parallel, delayed
from math import sqrt


def get_tree (cfg, src_files):
    client = bblfsh.BblfshClient("localhost:9432")

    x = []  
    for src_file in src_files:
        tree = client.parse(src_file).ast
        x.append(tree.internal_type)

    return x


if __name__ == "__main__":
    #client = bblfsh.BblfshClient("localhost:9432")

    file_path = "/Users/jayanti/Codes/Programs/Java/examples/HelloWorld.java"
    files = [file_path] * 1280 

    n = len(files)
    p = 8

    chunck_size = n /p 
    
    chuncks = []
    for i in range(0, p):
        chuncks.append(files[int(i*chunck_size):int((i+1)*chunck_size)])

    print(chuncks)


    #for i in range(0, 64):
    #    tree = client.parse(files[i]).ast
    #    print(i, tree)

    #x = [i for i in range(0,128)]
    p = 8
    r = 1280/p 

    cfg = None
    x= Parallel(n_jobs=8)(delayed(get_tree)(cfg, chuncks[i]) for i in range(p))


    #results = Parallel(n_jobs=-1, verbose=1, backend="threading")(
    #         map(delayed(myfun), arg_instances))


