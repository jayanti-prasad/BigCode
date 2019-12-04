import re
import itertools
import numpy as np 

class Tokenizer:
    def __init__(self, num_tokens):

       self.num_tokens = num_tokens 
       self.token2id = {}
       self.token_hist = {} 
       self.id2token = []
       self.vocab = [] 


    def fit(self, text_data):

        vocab = []
        token_hist = {}  
        for text in text_data :
            words = text.split()               
            for word in words:
                if word not in vocab:
                    vocab.append(word)
                if word not in token_hist:
                    token_hist [word] = 0
                token_hist [word] = token_hist [word] + 1 

        token_hist_sorted  = dict(sorted(token_hist.items(), key=lambda x: x[1], reverse=True))
        self.token_hist   = dict(itertools.islice(token_hist_sorted.items(), self.num_tokens-3))

        self.vocab = [x for x in  self.token_hist] 
        self.id2token = ["unk","__start__","__end__"] + [x for x in self.vocab]

        ids = [ str(i) for i in range(0, len(self.id2token))  ]

        self.token2id  = dict(zip(self.id2token, ids)) 
        

    def transform(self, text_data, text_len, padding=False, post=True, append_indicators=False):
        vec_data = [] 

        for text in text_data:

            words = text.split()[:text_len]
            vec = np.zeros(text_len, dtype=int)

            count = 0
            for j in range(0, len(words)):
                if j < text_len-2:
                    if  words[j] in self.id2token:
                       vec[j] =  self.token2id[words[j]]  
                    else:
                       vec[j] = 0      
                    count = count + 1 

            if append_indicators:
                 vec  = np.insert(vec, 0, 1, axis=0)
                 vec  = np.insert(vec, count+1, 2, axis=0)

            vec_data.append(vec)
              
        return np.array(vec_data) 

