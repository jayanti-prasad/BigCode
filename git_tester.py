import os
import re
import sys
import git
from unidiff import PatchSet

if __name__ == "__main__":

   repo = git.Repo(sys.argv[1])
   commits = list(repo.iter_commits())

   for i in range(len(commits)):
        diff = repo.git.diff(commits[i].hexsha, commits[i].hexsha+'^')
        patch_set = PatchSet(diff)
        for p in patch_set:
             if p.is_modified_file:
                 try:
                     if os.path.basename(p.path).split('.')[1] == 'java':
                         source_file = re.sub('^a\/', '', p.source_file)
                         target_file = re.sub('^b\/', '', p.target_file)
                         curr_code = repo.git.show('{}:{}'.format(commits[i].hexsha, source_file))
                         prev_code = repo.git.show('{}:{}'.format(commits[i].hexsha+'^', target_file))
                         for h in p:
                            l1, d1 =  h.target_start,  h.target_length
                            l2, d2 =  h.source_start, h.source_length                                               
                            print(commits[i].hexsha, commits[i].summary, source_file, l1, d1, l2, d2)
                 except:
                     pass  

