import sys
import re
import csv
import getpass
import argparse
from github import Github
from datetime import datetime
from pathlib import Path
import pandas as pd

"""
A program for crawling repos on github for a given language with at least
user given number of commits. 

"""
def github_crawler(username, password, language, min_commits, output_file = None):

    g = Github(username, password)

    time_limit = datetime.utcfromtimestamp(g.rate_limiting_resettime).strftime('%Y-%m-%d %H:%M:%S')
    print("You are logged in as :" + g.get_user().login)
    print("Your query limit :" + str(g.rate_limiting))
    print("Rate limit :" + str(g.get_rate_limit()))
    print("Time for rate limit to reset:" + time_limit)

    df = pd.DataFrame(columns=['repo_name','full_name','owner_name','git_url',\
       'language','num_commits','num_stars','num_forks','created_at','updated_at'])  

    repos = g.search_repositories(query='language:'+language)
    count = 0
    for r in repos:
        try:
           if r.get_commits().totalCount >  min_commits:
              df.loc[count] = [r.name, r.full_name, r.owner.login, r.html_url,\
                 r.language, r.get_commits().totalCount, r.stargazers_count, r.forks_count, r.created_at, r.updated_at]
              print(count, r.name, r.full_name, r.owner.login, r.git_url,\
                 r.language, r.get_commits().totalCount, r.stargazers_count, r.forks_count, r.created_at, r.updated_at) 
              count = count + 1
        except:
           pass 

    df["num_commits"] = pd.to_numeric(df["num_commits"])
    df = df.sort_values(by='num_commits', ascending=False)

    return df 

if __name__  == "__main__":
  
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='count')

    parser.add_argument('-u','--username', type = str, help = 'Github username')
    parser.add_argument('-p','--password', type = str, help = 'Github password')
    parser.add_argument('-n','--min-commits', type = int, help = 'Minimum comments')
    parser.add_argument('-l','--language', type = str, help = 'Language')
    parser.add_argument('-o','--output-file', type = str, help = 'Output filename')

    args = parser.parse_args()

    if args.password:
        password = args.password 
    else :
        password = getpass.getpass(prompt='Give Github password ?') 


    df = github_crawler(args.username, password, args.language, args.min_commits, args.output_file)

    df.to_csv(args.output_file)
 

