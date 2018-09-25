import os
import pandas as pd
import librosa
import glob

import numpy as np

import librosa.display
import matplotlib.pyplot as plt

import pickle

from scipy import spatial

def get_file_name():
	for dir_name, subdir_list, file_list in os.walk("downloads/"):
		dir_list = file_list

	return file_list

def extract_feature(music_list):
	feature_matrix = []

	counter = 0

	for music_file in music_list:
		full_path = "{}/{}".format("downloads/",music_file)
		data, sampling_rate = librosa.load(full_path)
		mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=64).T,axis=0)
		feature_matrix.append(mfccs)

	return np.array(feature_matrix)

def dump_feature():
	music_list = [name for name in get_file_name()]
	features = extract_feature(music_list)

	pickle.dump( features, open( "features.pickle", "wb" ) )

def dump_label():
	music_list = [name for name in get_file_name()]
	pickle.dump( music_list, open( "labels.pickle", "wb" ) )

def load_feature():
	with open("features.pickle","rb") as f:
		features = pickle.load(f)
	return features

def load_label():
	with open("labels.pickle","rb") as f:
		labels = pickle.load(f)
	return labels

def load_data():
	labels,features = (load_label(),load_feature())
	result = list(zip(labels,features))
	return result

class MF():

    def __init__(self, R, K, alpha, beta, iterations):
        """
        Perform matrix factorization to predict empty
        entries in a matrix.

        Arguments
        - R (ndarray)   : user-item rating matrix
        - K (int)       : number of latent dimensions
        - alpha (float) : learning rate
        - beta (float)  : regularization parameter
        """

        self.R = R
        self.num_users, self.num_items = R.shape
        self.K = K
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations

    def train(self):
        # Initialize user and item latent feature matrice
        self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))
        self.Q = np.random.normal(scale=1./self.K, size=(self.num_items, self.K))

        # Initialize the biases
        self.b_u = np.zeros(self.num_users)
        self.b_i = np.zeros(self.num_items)
        self.b = np.mean(self.R[np.where(self.R != 0)])

        # Create a list of training samples
        self.samples = [
            (i, j, self.R[i, j])
            for i in range(self.num_users)
            for j in range(self.num_items)
            if self.R[i, j] > 0
        ]

        # Perform stochastic gradient descent for number of iterations
        training_process = []
        for i in range(self.iterations):
            np.random.shuffle(self.samples)
            self.sgd()
            mse = self.mse()
            training_process.append((i, mse))
            if (i+1) % 10 == 0:
                print("Iteration: %d ; error = %.4f" % (i+1, mse))

        return training_process

    def mse(self):
        """
        A function to compute the total mean square error
        """
        xs, ys = self.R.nonzero()
        predicted = self.full_matrix()
        error = 0
        for x, y in zip(xs, ys):
            error += pow(self.R[x, y] - predicted[x, y], 2)
        return np.sqrt(error)

    def sgd(self):
        """
        Perform stochastic graident descent
        """
        for i, j, r in self.samples:
            # Computer prediction and error
            prediction = self.get_rating(i, j)
            e = (r - prediction)

            # Update biases
            self.b_u[i] += self.alpha * (e - self.beta * self.b_u[i])
            self.b_i[j] += self.alpha * (e - self.beta * self.b_i[j])

            # Update user and item latent feature matrices
            self.P[i, :] += self.alpha * (e * self.Q[j, :] - self.beta * self.P[i,:])
            self.Q[j, :] += self.alpha * (e * self.P[i, :] - self.beta * self.Q[j,:])

    def get_rating(self, i, j):
        """
        Get the predicted rating of user i and item j
        """
        prediction = self.b + self.b_u[i] + self.b_i[j] + self.P[i, :].dot(self.Q[j, :].T)
        return prediction

    def full_matrix(self):
        """
        Computer the full matrix using the resultant biases, P and Q
        """
        return self.b + self.b_u[:,np.newaxis] + self.b_i[np.newaxis:,] + self.P.dot(self.Q.T)

data = load_data()
R = []

for m in data:
	R.append(m[1])

R = np.array(R)
#R = (R / np.linalg.norm(R))


#
#mf = MF(R, K=5, alpha=0.1, beta=0.01, iterations=400)
#mf.train()

#result = np.array([[mf.get_rating(i,j) for j in range(0,R.shape[1])] for i in range(0,R.shape[0])])
#

P, D, Q = np.linalg.svd(R)
result = np.dot(np.dot(P[:,:13],np.diag(D)[:13,:13]),Q[:13,:])

data2, sampling_rate2 = librosa.load("testmp3/50TvhCxOyIc.mp3")
mfccs = np.mean(librosa.feature.mfcc(y=data2, sr=sampling_rate2, n_mfcc=64).T,axis=0)
#mfccs = (mfccs / np.linalg.norm(mfccs))

norm_list = []

for v in result:
    dist = 1-spatial.distance.cosine(v, mfccs)
    if dist < 0.997:
        norm_list.append(dist)

norm_list = np.array(norm_list)
max_idx = np.argmax(norm_list)

print(max_idx)
print(data[max_idx][0])
print(norm_list[max_idx])