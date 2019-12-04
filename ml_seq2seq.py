import os
import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()
import tensorflow.compat.v1.keras as keras 
import numpy as np
from shutil import rmtree

from tensorflow.compat.v1.keras.layers import Lambda, Dense, Input, Embedding, BatchNormalization, GRU
from tensorflow.compat.v1.keras.callbacks import CSVLogger, ModelCheckpoint, TensorBoard
from tensorflow.compat.v1.keras.models import Model
from tensorflow.compat.v1.keras import optimizers
from tensorflow.compat.v1.keras.utils import plot_model



class seq2seq_train:
    def __init__(self, cfg):
        self.cfg = cfg 
 
        self.enc_inp = None
        self.enc_outp = None
        self.dec_inp = None
        self.dec_outp = None
        self.enc_model = None
        self.model = None

        self.__get_model__()

    def __get_model__ (self):

        self.enc_inp = Input(shape=(self.cfg.input_seq_len(),), name="Encoder-Input")

        embd = Embedding(self.cfg.num_input_tokens(), self.cfg.latent_dim(),
            name='Encoder-Embedding', mask_zero=False)

        embd_outp = embd(self.enc_inp)

        x = BatchNormalization(name='Encoder-Batchnorm-1')(embd_outp)

        _, state_h = GRU(self.cfg.latent_dim(), return_state=True, name='Encoder-Last-GRU')(x)

        self.enc_model = Model(inputs=self.enc_inp, outputs=state_h,
            name='Encoder-Model')

        self.enc_outp = self.enc_model(self.enc_inp)

        self.cfg.logger.info("********** Encoder Model summary **************")
        self.cfg.logger.info(self.enc_model.summary())


        # get the decoder 

        self.dec_inp = Input(shape=(None,), name='Decoder-Input')

        dec_emb = Embedding(self.cfg.num_output_tokens(), self.cfg.latent_dim(),
                            name='Decoder-Embedding', mask_zero=False)(self.dec_inp)

        dec_bn = BatchNormalization(name='Decoder-Batchnorm-1')(dec_emb)

        decoder_gru = GRU(self.cfg.latent_dim(), return_state=True, return_sequences=True, name='Decoder-GRU')

        decoder_gru_output, _ = decoder_gru(dec_bn, initial_state=self.enc_outp)

        x = BatchNormalization(name='Decoder-Batchnorm-2')(decoder_gru_output)

        dec_dense = Dense(self.cfg.num_output_tokens(), activation='softmax', name='Final-Output-Dense')

        self.dec_outp = dec_dense(x)

        model_inp = [self.enc_inp, self.dec_inp]

        self.model = Model(model_inp, self.dec_outp)

        self.cfg.logger.info("********** Full Model summary **************")

        self.cfg.logger.info(str(self.model.summary()))

        plot_model(self.model, to_file = self.cfg.scratch_dir() + os.sep + "seq2seq.png")


    def fit_model(self, input_vecs, output_vecs):

         input_data = [input_vecs,  output_vecs[:, :-1]]
         output_data = output_vecs[:, 1:]

         self.model.compile(optimizer=optimizers.Nadam(lr=0.001),
            loss='sparse_categorical_crossentropy', metrics=['accuracy'])

         model_checkpoint = ModelCheckpoint(self.cfg.output_dir() + os.sep +  'model.hdf5',
                                           monitor='val_loss', save_best_only=True, period=1)

         csv_logger = CSVLogger(self.cfg.log_dir() + os.sep + 'history.csv')
         tb_dir =  self.cfg.log_dir() + os.sep + "tensorboard"

         if os.path.isfile(tb_dir):
            rmtree(tb_dir)

         tensorboard = TensorBoard(log_dir = tb_dir,
            histogram_freq =10, batch_size =self.cfg.batch_size(),
            write_graph =True, write_grads =False, write_images =False,
            embeddings_freq =0, embeddings_layer_names=None, embeddings_metadata= None,
            embeddings_data =None)

         history = self.model.fit(input_data, np.expand_dims(output_data, -1),
                  batch_size =self.cfg.batch_size(),
                  epochs =self.cfg.nepochs(), validation_split=self.cfg.validation_split(),
                  callbacks=[csv_logger, model_checkpoint, tensorboard])


         return (history)
