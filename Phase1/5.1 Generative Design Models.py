import tensorflow as tf
from tensorflow.keras import layers, models
import torch
import torch.nn as nn


class BuildingVAE(tf.keras.Model):
    """Variational Autoencoder for building design generation"""

    def __init__(self, latent_dim=50):
        super(BuildingVAE, self).__init__()
        self.latent_dim = latent_dim

        # Encoder
        self.encoder = tf.keras.Sequential([
            layers.Dense(512, activation='relu'),
            layers.Dense(256, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(latent_dim * 2)  # mean and log_var
        ])

        # Decoder
        self.decoder = tf.keras.Sequential([
            layers.Dense(128, activation='relu'),
            layers.Dense(256, activation='relu'),
            layers.Dense(512, activation='relu'),
            layers.Dense(100, activation='sigmoid')  # Building parameters
        ])

    def encode(self, x):
        mean, log_var = tf.split(self.encoder(x), num_or_size_splits=2, axis=1)
        return mean, log_var

    def reparameterize(self, mean, log_var):
        eps = tf.random.normal(shape=mean.shape)
        return eps * tf.exp(log_var * 0.5) + mean

    def decode(self, z):
        return self.decoder(z)


class EnergyPredictionModel:
    """Neural network for energy consumption prediction"""

    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(50,)),
            layers.Dropout(0.2),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='linear')  # Energy consumption output
        ])

        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )

        return model

    def train(self, building_features, energy_targets):
        """Train the energy prediction model"""
        return self.model.fit(
            building_features,
            energy_targets,
            epochs=100,
            batch_size=32,
            validation_split=0.2,
            verbose=1
        )

    def predict_energy_consumption(self, building_params):
        """Predict energy consumption for building parameters"""
        return self.model.predict(building_params)