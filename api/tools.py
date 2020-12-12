import librosa
from scipy import signal
import numpy as np
import tensorflow as tf
import os
from tensorflow import keras


def load_model(path):
    model = keras.models.load_model(path)

    return model


def read_audio(path):
    audio = librosa.load(os.path.join(path), 44100)
    div_fac = 1 / np.max(np.abs(audio)) / 3.0
    audio = audio * div_fac

    return audio


def prepare_input_features(stft_features):
    noisySTFT = np.concatenate(
        [stft_features[:, 0:8 - 1], stft_features], axis=1)
    stftSegments = np.zeros(
        (2049, 8, noisySTFT.shape[1] - 8 + 1))
    for index in range(noisySTFT.shape[1] - 8 + 1):
        stftSegments[:, :, index] = noisySTFT[:, index:index + 8]
    return stftSegments


def perform_istft(audio_path):
    model = load_model('model.h5')
    inputAudio = read_audio(audio_path)
    stftFeatures = librosa.stft(inputAudio, 4096, 4096, 1024,
                                scipy.signal.hamming(4096, sym=False),
                                center=True)
    predictors = prepare_input_features(stftFeatures)
    print(predictors.shape)
    networkOutput = model.predict(predictors)
    return librosa.istft(networkOutput[:, :, -1], 4096, 1024,
                  scipy.signal.hamming(4096, sym=False), center=True)
