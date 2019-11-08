import sys
import os
import pandas as pd

class ConfigParallel:
    def __init__(self, cfg_parser):
        self.cfg_parser = cfg_parser
        self.issue_key =  None 
        self.logfile = None

    def workspace_dir(self):
        work_dir = self.cfg_parser.get('input', 'workspace_dir')
        os.makedirs(work_dir, exist_ok=True)
        return work_dir 

    def download_dir(self):
        down_dir = self.cfg_parser.get('input', 'download_dir')
        os.makedirs(down_dir, exist_ok=True)
        return down_dir 

    def output_dir(self):
        tmp_dir = self.workspace_dir() + os.sep + "output"
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir 

    def scratch_dir(self):
        tmp_dir = self.workspace_dir() + os.sep + "scratch"
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir  

    def log_dir(self):
        tmp_dir = self.workspace_dir() + os.sep + "log"
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir 
 
    def project_src_dir(self):
        return self.download_dir() + os.sep + self.proj['project_name']

    def project_git_dir(self):
        return self.download_dir() + os.sep + self.proj['project_name'] + os.sep +".git"

    def project_scratch_dir(self):
        tmp_dir = self.scratch_dir() + os.sep + self.proj['project_name'] 
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir 

    def load_project(self, proj):
        self.proj  = proj   
        self.repo  = None 

    def ast_flag(self):
        return self.cfg_parser.get('input', 'ast_flag')

    def lang_type(self):
        data = self.cfg_parser.get('input', 'lang_type')
        return(data.split(","))

    def log_level(self):
        return self.cfg_parser.get('input', 'log_level')
   
    def get_repos_list_file(self):
        return self.cfg_parser.get('input', 'github_repos_file')

    def jira_issues_dir(self):
        tmp_dir = self.cfg_parser.get('input', 'jira_issues_dir')
        os.makedirs(tmp_dir, exist_ok=True)
        return tmp_dir 

    def get_projects(self):
        repos_file = self.get_repos_list_file()
        df_repos  = pd.read_csv(repos_file) 
        return df_repos.to_dict('records')

    def ast_server(self):
        return self.cfg_parser.get('input', 'ast_server')
  
    def ast_client(self):
        return  astclient.AstClient(self.ast_server())

    def columns(self):
        data=self.cfg_parser.get('input', 'columns')
        return(data.split(","))

    def use_jira_issues(self):
        return self.cfg_parser.getboolean('input', 'use_jira_issues')

    def get_commit_info(self):
        return self.cfg_parser.getboolean('input', 'get_commit_info')

    def dump_source_files(self):
        return self.cfg_parser.getboolean('input', 'dump_source_files')

    def dump_ast_files(self):
        return self.cfg_parser.getboolean('input', 'dump_ast_files')   

    def max_files_changed(self):
        return int(self.cfg_parser.get('settings', 'max_files_changed'))

    def max_hunks_changed(self):
        return int(self.cfg_parser.get('settings', 'max_hunks_changed'))

    def max_hunk_size(self):
        return int(self.cfg_parser.get('settings', 'max_hunk_size'))

    def num_processes(self):
        return int(self.cfg_parser.get('settings', 'num_processes'))

