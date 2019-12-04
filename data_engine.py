import os
import re
import pandas as pd
import numpy as np
import pickle
from unidiff import PatchSet
from ast_model import Tree 
from ast_diff import AstDiff 

def get_filename(file_path, D , tag):
    filename = file_path.split('/')
    prefix = filename[-1].split('.')[0]
    suffix = filename[-1].split('.')[1]
    full_filename = D['project_name'] + "_" +\
       D['commit_id'] + "_" + prefix + "_" + tag + "." + suffix 
    return full_filename 



def write_source_files(prev_code, curr_code, prev_file_name, curr_file_name, cfg):
    with open(cfg.project_scratch_dir() + os.sep + prev_file_name, "w") as fp:
        fp.write(prev_code)
    with open(cfg.project_scratch_dir() + os.sep + curr_file_name, "w") as fp:
        fp.write(curr_code)
    cfg.logger.info("source files written")



def write_ast_files(prev_ast, curr_ast, prev_file_name, curr_file_name, cfg):
    prev_ast_file = prev_file_name.split(".")[0] + ".ast"
    curr_ast_file = curr_file_name.split(".")[0] + ".ast"
    with open(cfg.project_scratch_dir() + os.sep + prev_ast_file,"wb") as fp:
         pickle.dump(prev_ast.anytree, fp)
    with open(cfg.project_scratch_dir() + os.sep + curr_ast_file,"wb") as fp:
         pickle.dump(curr_ast.anytree, fp)
    cfg.logger.info("ast files written")



def get_commits_data(w, cfg, commits, return_dict):
    repo = cfg.repo
    df = pd.DataFrame(columns=cfg.columns(), dtype=str)
    num_commits = len(commits)
    count = 0
    cfg.logger.info("process id:" + str(w) + "number of commits:" + str(len(commits)))

    for i in range(0, num_commits):
        D = {}
        D['project_name'] = cfg.proj['project_name']
        D['commit_msg'] = commits[i].summary
        D['commit_id'] = commits[i].hexsha

        cfg.logger.info("Processing [" + str(i) + "/" + str(num_commits) + "]: " + D['commit_id'])
    
        try:  
            diff = repo.git.diff(commits[i].hexsha, commits[i].hexsha+'^')
            patch_set = PatchSet(diff)
        except:
            diff, patch_set  = None, []  
            cfg.logger.info("Failed to get diff :" + commits[i].hexsha)
            pass   

        if len(patch_set) <=  cfg.max_files_changed() and diff:
            for p in patch_set:
                if p.is_modified_file:
                    if len(p) <=  cfg.max_hunks_changed():
                        try:                      
                           file_type = os.path.basename(p.path).split('.')[1]
                        except:
                           file_type = None  
                        if file_type == 'java':

                            try:
                                source_file = re.sub('^a\/', '', p.source_file)
                                target_file = re.sub('^b\/', '', p.target_file)

                                D['file_name'] = source_file           
                                curr_code = repo.git.show('{}:{}'.format(commits[i].hexsha, source_file))
                                prev_code = repo.git.show('{}:{}'.format(commits[i].hexsha+'^', target_file))

                                prev_file_name = get_filename(p.source_file, D, 'prev')
                                curr_file_name = get_filename(p.target_file, D, 'curr')

                                write_source_files(prev_code, curr_code, prev_file_name, curr_file_name, cfg)
                            except:
                                prev_code, curr_code, prev_file_name, curr_file_name = None, None, None, None 
                                cfg.logger.info("Failed to get prve & curr code")
                                pass  

                            try:
                                cfg.logger.info("getting ast for: " +  prev_file_name)
                                prev_ast = Tree (cfg.project_scratch_dir() + os.sep + prev_file_name, cfg) 
                                curr_ast = Tree (cfg.project_scratch_dir() + os.sep + curr_file_name, cfg) 
                            except:
                                prev_ast, curr_ast = None, None 
                                cfg.logger.info("Failed to get ast tree !") 
                                pass 
 

                            if prev_ast and curr_ast:
  
                                write_ast_files(prev_ast, curr_ast, prev_file_name, curr_file_name, cfg)

                                prev_data =  AstDiff(prev_code, prev_ast) 
                                curr_data =  AstDiff(curr_code, curr_ast)              
                            
                                for h in p:
                                    
                                    if np.max([h.source_length, h.target_length]) < cfg.max_hunk_size():
                                        prev_raw, prev_ast = prev_data.get_ast_seq(h.target_start, h.target_start + h.target_length)
                                        curr_raw, curr_ast = curr_data.get_ast_seq(h.source_start, h.source_start + h.source_length)
  
                                        data = [cfg.proj['project_name'],commits[i].hexsha,commits[i].summary,
                                            source_file,prev_raw,curr_raw,prev_ast,curr_ast,h.target_start,h.target_length,
                                            h.source_start,h.source_length]
                     
                                        df.loc[count]=data 
                                        count = count + 1

    cfg.logger.info("[commit_data] for thread " + str(w) + " number of rows in the data frame :" + str(count))
    return_dict[w] = df 
    return df 

