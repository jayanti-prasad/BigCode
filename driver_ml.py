import argparse
import configparser
import config_ml 

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

    cfg = config_bc.ConfigBigCode(cfg_parser)

    for section_name in cfg_parser:
        print('Section:', section_name)
        section = cfg_parser[section_name]
        for name in section:
            print('  {} = {}'.format(name, section[name]))
        print()


