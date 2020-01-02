import argparse
import configparser
import config_ml 
from ml_seq2seq import seq2seq_train 
from tokenizer import Tokenizer
from data_utils import get_training_data

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

    cfg = config_ml.ConfigML(cfg_parser)

    for section_name in cfg_parser:
        print('Section:', section_name)
        section = cfg_parser[section_name]
        for name in section:
            print('  {} = {}'.format(name, section[name]))
        print()


    # get the data   
    x_train, y_train = get_training_data (cfg)


    # get the model 
    M = seq2seq_train(cfg)

    # fit the model 

    h = M.fit_model(x_train, y_train)

