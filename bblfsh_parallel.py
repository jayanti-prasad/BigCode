from concurrent import futures
import bblfsh
import sys
from joblib import Parallel, delayed
import pandas as pd 


def get_chuncks (data, np):
    chunck_size = int(len(data)/np) 
    chuncks = []
    for i in range(np):
        chunck_start =  i *  chunck_size
        chunck_end = (i+1) * chunck_size
        chuncks.append(data[chunck_start:chunck_end])

    return chuncks 


def run (cfg, src_files):
    client =  bblfsh.BblfshClient("localhost:9432")

    df = pd.DataFrame(columns=['internal_type'])
    x = []
    count = 0
    for src_file in src_files:
        tree = client.parse(src_file).uast
        #x.append(tree.internal_type)
        df.loc[count] = [tree.internal_type]
        count = count + 1 
    return df

if __name__ == "__main__":


    file_path = "/Users/jayanti/Codes/Programs/Java/examples/HelloWorld.java"
    n = 1280 
    p = 8
    files = [file_path] * n 

    chuncks = get_chuncks (files, p)

    cfg = None 
    y = Parallel(n_jobs=p)(delayed(run)(cfg, chuncks[i]) for i in range(p))
        
