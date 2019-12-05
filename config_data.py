import sys
import os
import pandas as pd
from logutil import get_logger
from concurrent import futures
from anytree import Node
import bblfsh
import hashlib
import re



class ConfigBigCode:
    def __init__(self, cfg_parser):
        self.cfg_parser = cfg_parser
        self.logfile = None
        self.logger = get_logger("big-code", self.log_dir(), self.log_file(),
            log_level=self.log_level(), log_to_console=True)

    def workspace_dir(self):
        work_dir = self.cfg_parser.get('settings', 'workspace_dir')
        os.makedirs(work_dir, exist_ok=True)
        return work_dir 

    def download_dir(self):
        down_dir = self.cfg_parser.get('settings', 'download_dir')
        os.makedirs(down_dir, exist_ok=True)
        return down_dir 

    def ast_server(self):
        return self.cfg_parser.get('settings', 'ast_server')

    def columns(self):
        data=self.cfg_parser.get('settings', 'columns')
        return(data.split(","))

    def num_processes(self):
        return int(self.cfg_parser.get('settings', 'num_processes'))

    def max_files_changed(self):
        return int(self.cfg_parser.get('settings', 'max_files_changed'))

    def max_hunks_changed(self):
        return int(self.cfg_parser.get('settings', 'max_hunks_changed'))

    def max_hunk_size(self):
        return int(self.cfg_parser.get('settings', 'max_hunk_size'))

                                                                                     
    def projects_list_file(self):
        return self.cfg_parser.get('settings', 'projects_list_file')

    def log_level(self):
        return self.cfg_parser.get('log', 'log_level')

    def log_file(self):
        return self.cfg_parser.get('log', 'log_file')



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

    def get_projects(self):
        repos_file = self.projects_list_file()
        df_repos  = pd.read_csv(repos_file) 
        return df_repos.to_dict('records')

    def ast_client(self):
        return  bblfsh.BblfshClient(self.ast_server())


