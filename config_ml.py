import sys
import os
import pandas as pd
from logutil import get_logger

class ConfigML:
    def __init__(self, cfg_parser):
        self.cfg_parser = cfg_parser
        self.logfile = None

        self.logger = get_logger("big-code", self.log_dir(), self.log_file(),
            log_level=self.log_level(), log_to_console=True)

    def workspace_dir(self):
        work_dir = self.cfg_parser.get('settings', 'workspace_dir')
        os.makedirs(work_dir, exist_ok=True)
        return work_dir 

     
    def input_data__dir(self):
        return  self.cfg_parser.get('settings', 'input_data_dir')


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


    def nepochs(self):
        return  self.cfg_parser.getint('training', 'nepochs')


    def batch_size(self):
        return self.cfg_parser.getint('training', 'batch_size')


    def random_seed(self):
        return  self.cfg_parser.getint('training', 'random_seed')


    def test_train_split(self):
        return  self.cfg_parser.getfloat('training', 'test_train_split')


    def validation_split(self):
        return  self.cfg_parser.getfloat('training', 'validation_split')


    def num_input_tokens(self):
        return  self.cfg_parser.getint('model-seq2seq', 'num_input_tokens')

    def num_output_tokens(self):
        return  self.cfg_parser.getint('model-seq2seq', 'num_output_tokens')

    def input_seq_len(self):
        return  self.cfg_parser.getint('model-seq2seq', 'input_seq_len')

    def output_seq_len(self):
        return  self.cfg_parser.getint('model-seq2seq', 'output_seq_len')

    def input_col(self):
        return  self.cfg_parser.get('model-seq2seq', 'input_col')

    def output_col(self):
        return  self.cfg_parser.get('model-seq2seq', 'output_col')

