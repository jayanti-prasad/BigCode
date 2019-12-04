import os
import glob 
import re 
import pandas as pd 
from tokenizer import Tokenizer  
from sklearn.model_selection import train_test_split

def clean_text (text_data):
   text_data =  [re.sub('\d+:','', x)  for x in input_text_data]
   text_data =  [re.sub('\n','', x)  for x in text_data]
   return  text_data 

def get_training_data (cfg):
    if cfg.input_data_dir():
        filenames = glob.glob(cfg.input_data_dir() + os.sep + "*.csv")
        for f in filenames:
            cfg.logger.info("reading and combining  files:" + f)
        df = pd.concat([pd.read_csv(f) for f in filenames])
    else:
        cfg.logger.info("No training data dir provided")
        sys.exit()

    cfg.logger.info("input data frame:" + str(df.shape))

    df = df.astype(str)

    df_train, df_test = train_test_split(df, test_size =\
        cfg.test_train_split(), random_state=cfg.random_seed())

    x = df[cfg.input_col()].tolist()
    y = df[cfg.output_col()].tolist()

    input_pp  = Tokenizer (cfg.num_input_tokens())
    output_pp  = Tokenizer (cfg.num_output_tokens())

    input_pp.fit(x)
    output_pp.fit(y)

    x_train = df_train[cfg.input_col()].tolist()
    y_train = df_train[cfg.output_col()].tolist()

    input_vecs  = input_pp.transform(x_train, cfg.input_seq_len(),\
        padding=True, post=False, append_indicators=False)  

    output_vecs = output_pp.transform(y_train, cfg.output_seq_len(),\
        padding=True, post=True, append_indicators=True)  

    return input_vecs, output_vecs 

