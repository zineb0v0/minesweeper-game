from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten
from tensorflow.keras.optimizers import Adam

def create_dqn(learn_rate, input_dims, n_actions, conv_units, dense_units):
    model = Sequential([
                Conv2D(conv_units, (3,3), activation='relu', padding='same', input_shape=input_dims),
                Conv2D(conv_units, (3,3), activation='relu', padding='same'),
                Conv2D(conv_units, (3,3), activation='relu', padding='same'),
                Conv2D(conv_units, (3,3), activation='relu', padding='same'),
                Flatten(),
                Dense(dense_units, activation='relu'),
                Dense(dense_units, activation='relu'),
                Dense(n_actions, activation='linear')])

    model.compile(optimizer=Adam(learning_rate=learn_rate, epsilon=1e-4), loss='mse')

    return model
