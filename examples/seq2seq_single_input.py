import os
import sys
import argparse  
import numpy as np
import tensorflow.compat.v1.keras as keras 
from  tensorflow.compat.v1.keras.layers import Input, Embedding, BatchNormalization, GRU, Dense 
from  tensorflow.compat.v1.keras.models import Model 
from  tensorflow.compat.v1.keras.callbacks import  


def get_encoder_model (cfg):
    encoder_inputs  = Input(shape=(cfg.len_input_seq,), 
       name='Encoder-Input')

    x = keras.layers.Embedding(cfg.num_input_tokens, cfg.latent_dim,
       name='Encoder-Embedding', mask_zero=False) (encoder_inputs)

    x = keras.layers.BatchNormalization(name='Encoder-Batchnorm-1')(x)

    _, state_h = keras.layers.GRU(cfg.latent_dim, return_state=True,\
       name='Encoder-Last-GRU')(x)

    encoder_model = keras.models.Model(inputs=encoder_inputs,
       outputs=state_h, name='Encoder-Model')
    
    encoder_outputs = encoder_model(encoder_inputs)
 
    return encoder_model, encoder_inputs, encoder_outputs   


def get_model (cfg, encoder_inputs, encoder_outputs):
 
    decoder_inputs = keras.layers.Input(shape=(None,), 
       name='Decoder-Input')  # for teacher forcing

    dec_emb = keras.layers.Embedding(cfg.num_input_tokens, cfg.latent_dim,
       name='Decoder-Embedding', mask_zero=False)(decoder_inputs)

    dec_bn = keras.layers.BatchNormalization(name='Decoder-Batchnorm-1')(dec_emb)

    decoder_gru = keras.layers.GRU(cfg.latent_dim, return_state=True,
       return_sequences=True, name='Decoder-GRU')

    decoder_gru_output, _ = decoder_gru(dec_bn, initial_state=encoder_outputs)

    x = keras.layers.BatchNormalization(name='Decoder-Batchnorm-2')(decoder_gru_output)
    decoder_dense = keras.layers.Dense(cfg.num_output_tokens, 
       activation='softmax', name='Final-Output-Dense')

    decoder_outputs = decoder_dense(x)

    model = keras.models.Model([encoder_inputs, decoder_inputs], decoder_outputs)    
 
    return model 


def fit_model (cfg, model, X, Y):

    model.compile(optimizer=keras.optimizers.Nadam(lr=0.01),
           loss='sparse_categorical_crossentropy',metrics=['acc'])

    encoder_input_data = X
    decoder_input_data = Y[:, :-1]
    decoder_output_data = Y[:, 1:]
    
    model_checkpoint = keras.callbacks.ModelCheckpoint(cfg.workspace + os.sep + 'model.hdf5',
         monitor='val_loss', save_best_only=True, period=1)


    history =   model.fit([encoder_input_data,
                decoder_input_data],  np.expand_dims(decoder_output_data, -1),
                batch_size =100,
                epochs = cfg.epoch, validation_split = 0.12,
                callbacks= [model_checkpoint])  

    return history 


 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='cmod')
    parser.add_argument('-itn', '--num_input_tokens',type=int,
        help='Number of input tokens', required=True)
    parser.add_argument('-otn', '--num_output_tokens',type=int, 
        help='Number of output tokens', required=True)
    parser.add_argument('-isl', '--len_input_seq',type=int, 
        help='Length of input sequence', required=True)
    parser.add_argument('-osl', '--len_output_seq',type=int, 
        help='Length of input sequence', required=True)
    parser.add_argument('-ldm', '--latent_dim',type=int, 
        help='Latent dimension', required=True)
    parser.add_argument('-n', '--epoch', type=int,
        help='Epochs', required=True)
    parser.add_argument('-w', '--workspace',
        help='Output Directory', required=True)

    cfg = parser.parse_args()

    os.makedirs (cfg.workspace, exist_ok=True)
    
    encoder_model, encoder_inputs, encoder_outputs  = get_encoder_model (cfg)

    print(encoder_model.summary())
    keras.utils.plot_model(encoder_model, to_file = cfg.workspace + os.sep + "encoder.png")

    model = get_model (cfg, encoder_inputs, encoder_outputs)  
    print(model.summary())
    keras.utils.plot_model(model, to_file = cfg.workspace + os.sep + "model.png")
 
    # create fake data
    X  =  np.random.randint(cfg.num_input_tokens,
       size=(1000, cfg.len_input_seq))

    Y  =  np.random.randint(cfg.num_output_tokens,
       size=(1000, cfg.len_output_seq))

    print(X.shape)
    print(Y.shape)

    # fit the model 
    h = fit_model (cfg, model, X, Y) 

