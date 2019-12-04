import os
import sys
import pathlib
import argparse
import configparser
from importlib import reload
import logutil
import logging
import config_data
from data_engine import get_commits_data 
import git
import shutil


def run(cfg, p):
    cfg.load_project(p)

    logging.shutdown()
    reload(logging)
  
    p['project_name'] = p['project_url'].split('/')[-1] 
    p['org_name'] = p['project_url'].split('/')[-2] 

    file_prefix = p['org_name'] + "_" + p['project_name']

    commits_info_file = cfg.output_dir() + os.sep + file_prefix + "_info" + ".csv"
    commits_data_file = cfg.output_dir() + os.sep + file_prefix + "_data" + ".csv"
    proj_log_file = file_prefix + ".log"

    cfg.logger = logutil.get_logger("cmod_parallel_log", cfg.log_dir(), 
        proj_log_file, cfg.log_level())

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
        logger.info("commit data  file exists, not processing for project:" + p['project_name'])
    else:
        #df_commits_data = parallel_process(cfg, get_commits_data, commits)
        df_commits_data = get_commits_data(0, cfg, commits, {})
         
        df_commits_data.to_csv(commits_data_file, sep=',')
        logger.info("Commits data  written in :" + commits_data_file)

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
   
    for section_name in cfg_parser:
        print('Section:', section_name)
        section = cfg_parser[section_name]
        for name in section:
            print('  {} = {}'.format(name, section[name]))
        print()


    logger = logutil.get_logger('cmod_parallel',  cfg.log_dir(), 'cmod_paralle.log', cfg.log_level())

    if args.erase:
        logger.info("Deleting output, scratch, log dirs")
        shutil.rmtree(cfg.output_dir())  
        shutil.rmtree(cfg.scratch_dir())  
        shutil.rmtree(cfg.log_dir())  


    if cfg.projects_list_file():
        proj_list = cfg.get_projects()
    else:
        logger.info("provide a git repos file created by github crawler [github_crawler.py] ")
        sys.exit()      

    for p in proj_list:
        run(cfg, p)
