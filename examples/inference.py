import os
import sys
import argparse  
import numpy as np
import tensorflow.compat.v1.keras.layers as layers
import tensorflow.compat.v1.keras.models as models
import tensorflow.compat.v1.keras.utils  as utils
import tensorflow.compat.v1.keras.optimizers as optimizers
import tensorflow.compat.v1.keras.callbacks as callbacks

def get_decoder_model (model):

    latent_dim = model.get_layer('Decoder-Embedding').output_shape[-1]
        
    decoder_inputs = model.get_layer('Decoder-Input').input
    dec_emb = model.get_layer('Decoder-Embedding')(decoder_inputs)
    dec_bn = model.get_layer('Decoder-Batchnorm-1')(dec_emb)
        
    gru_inference_state_input = layers.Input(shape=(latent_dim,),
       name='hidden_state_input')
 
    gru_out, gru_state_out = model.get_layer('Decoder-GRU') \
       ([dec_bn, gru_inference_state_input])

    dec_bn2 = model.get_layer('Decoder-Batchnorm-2')(gru_out)
    dense_out = model.get_layer('Final-Output-Dense')(dec_bn2)
    decoder_model = models.Model([decoder_inputs, gru_inference_state_input],
                                   [dense_out, gru_state_out])
    return decoder_model 


def load_model (cfg):

    model = models.load_model(cfg.workspace + os.sep + "model.hdf5")

    encoder_model = model.get_layer('Encoder-Model')

    decoder_model = get_decoder_model (model)
     
    return encoder_model, decoder_model, model 


def predict_seq (cfg, encoder_model, decoder_mode, X):

    start_token = 0 
    start_token = 10 
   
    embd_vec = encoder_model.predict(X)

    state_value =  start_token 

    decoded_sentence = []
    stop_condition = False

    while not stop_condition:

         preds, st = decoder_model.predict([state_value, embd_vec])

         # We are going to ignore indices 0 (padding) and indices 1 (unknown)
         # Argmax will return the integer index corresponding to the
         #  prediction + 2 b/c we chopped off first two

         pred_idx = np.argmax(preds[:, :, 2:]) + 2

         if pred_idx== end_token  or len(decoded_sentence) >=  cfg.max_target_seq:
               stop_condition = True
               break
         decoded_sentence.append(pred_idx)

         # update the decoder for the next word
         embd_vec = st
         state_value = np.array(pred_idx).reshape(1, 1)

    return decoded_sentence 


 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='cmod')
    parser.add_argument('-w', '--workspace', help='Output Directory', required=True)

    cfg = parser.parse_args()

    encoder_model, decoder_model, model  = load_model (cfg)

    print(encoder_model.summary())
    utils.plot_model(encoder_model, to_file = cfg.workspace + os.sep + "infr_encoder.png")

    print(decoder_model.summary())
    utils.plot_model(decoder_model, to_file = cfg.workspace + os.sep + "infr_decoder.png")

    print(model.summary())
    utils.plot_model(model, to_file = cfg.workspace + os.sep + "infr_model.png")
 


