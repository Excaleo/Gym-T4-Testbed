import sys
import os
import numpy as np
from keras.layers import Conv2D, Dense, Input, Flatten
from keras.models import Model
from keras.optimizers import Adam
from keras import losses
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from world_model.load_world_model import load_world_model
from utils import encode_action, preprocess_frame
from world_model.simple_vae import CVAE

INPUT_DIM = (80,104,1)

class StateAgent():
    def __init__(self,action_dim,env_name):
        self.action_dim = action_dim
        self.model = self.build_model(action_dim)
        self.world_model = load_world_model(env_name,action_dim)

    def build_model(self, action_dim):
        frame_input = Input(shape=(INPUT_DIM[1],INPUT_DIM[0],INPUT_DIM[2]*self.action_dim))
        
        conv_1 = Conv2D(filters=32, kernel_size=5, strides=2, activation='relu')(frame_input)
        conv_2 = Conv2D(filters=64, kernel_size=5, strides=2, activation='relu')(conv_1)
        conv_3 = Conv2D(filters=64, kernel_size=5, strides=2, activation='relu')(conv_2)
        flatten = Flatten(name='flatten')(conv_3)
        dense = Dense(256)(flatten)
        output = Dense(action_dim, activation="sigmoid")(dense)

        optimizer = Adam(lr=0.0003)
        model = Model(frame_input, output)

        model.compile(optimizer=optimizer, loss = losses.binary_crossentropy)
        model.summary()
        return model
    
    def train(self, input_states, output_label):
        self.model.fit(x=input_states,
                       y=output_label,
                       shuffle=True,
                       epochs=32,
                       batch_size=32)
    
    def set_weights(self, filepath):
        self.model.load_weights(filepath)
    
    def save_weights(self, filepath):
        self.model.save_weights(filepath)

    def predict(self, input_state):
        # next_states = self.world_model.generate_output_states(input_state)
        return self.model.predict(input_state)




