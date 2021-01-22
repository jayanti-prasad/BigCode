import os
import git
import pathlib
import shutil
import logging
import argparse
import configparser
import pandas as pd
from joblib import Parallel, delayed
from importlib import reload
import logutil
import config_data
from data_engine import get_commits_data


def get_chuncks (cfg, data):
    chunck_size = int(len(data)/cfg.num_processes())
    chuncks = []
    for i in range(cfg.num_processes()):
        chunck_start =  i *  chunck_size
        chunck_end = (i+1) * chunck_size
        chuncks.append([chunck_start,chunck_end])

    return chuncks


def run(cfg, p):
    cfg.load_project(p)

    logging.shutdown()
    reload(logging)

    p['project_name'] = p['git_url'].split('/')[-1] 
    p['org_name'] = p['git_url'].split('/')[-2] 
    p['project_url'] = p['git_url']
    file_prefix = p['org_name'] + "_" + p['project_name']

    commits_data_file = cfg.output_dir() + os.sep + file_prefix + "_data" + ".csv"

    if pathlib.Path(cfg.project_git_dir()).exists():
        cfg.logger.info("git repo found for project:" + p['project_name'])
    else:
       cfg.logger.info("no git data found for project:" + p['project_name'])
       cfg.logger.info("downloading git data for :" + p['project_name'])
       git.Git(cfg.download_dir()).clone(p['project_url'])
       
    cfg.repo = git.Repo(cfg.project_git_dir())
   
    commits = list(cfg.repo.iter_commits())
    cfg.logger.info("Number of commits to process :" + str(len(commits)))

    if pathlib.Path(commits_data_file).exists():
        cfg.logger.info("commit data  file exists, not processing for project:" + p['project_name'])
    else:
        chuncks = get_chuncks (cfg, commits) 

        dfs = Parallel(n_jobs=cfg.num_processes())(delayed(get_commits_data) \
            (cfg, chuncks[i]) for i in range(cfg.num_processes()))
        # join all the dataframes  
        dF = pd.concat(dfs)     
        dF.to_csv(commits_data_file, sep=',')
        cfg.logger.info("Commits data  written in :" + commits_data_file)

if __name__ == "__main__":

    """
    Main driver program to launch the parallel pipeline for processing 
    github commits. 
    """

    parser = argparse.ArgumentParser(description='cmod')
    parser.add_argument('-c', '--config', help='Config file path', required=True)
    parser.add_argument('-e', '--erase', help='Clean previous run data', action='store_true')

    cfg_parser = configparser.ConfigParser()
    args = parser.parse_args()
    cfg_parser.read(args.config)

    cfg = config_data.ConfigBigCode(cfg_parser)

    
    if args.erase:
        cfg.logger.info("Deleting output, scratch, log dirs")
        shutil.rmtree(cfg.output_dir())
        shutil.rmtree(cfg.scratch_dir())

   
    for section_name in cfg_parser:
        cfg.logger.info('Section:' +  section_name)
        section = cfg_parser[section_name]
        for name in section:
            cfg.logger.info('  {} = {}'.format(name, section[name]))
        cfg.logger.info("")


    if cfg.projects_list_file():
        proj_list = cfg.get_projects()
    else:
        cfg.logger.info("provide a git repos file created by github crawler [github_crawler.py] ")
        sys.exit()      

    for p in proj_list:
        run(cfg, p)
