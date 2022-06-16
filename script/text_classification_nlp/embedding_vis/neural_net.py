"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/6/16 7:48 PM
"""

from gensim.models import word2vec
import re
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


class NeuralNetwork:
    def __init__(self, X, y, words_indices: dict):
        self.N = 10
        self.X_train = X
        self.y_train = y
        self.window_size = 2
        self.alpha = 0.01
        self.words_indices = words_indices
        self.vocabulary = list(words_indices.keys())
        np.random.seed(100)

        self.W = np.random.uniform(-0.8, 0.8, (len(self.vocabulary), self.N))
        self.W1 = np.random.uniform(-0.8, 0.8, (self.N, len(self.vocabulary)))

    def forward_propagation(self, X):
        self.h = np.dot(self.W.T, X).reshape(self.N, 1)
        self.u = np.dot(self.W1.T, self.h)
        self.y = softmax(self.u)
        return self.y

    def backward_propagation(self, x, t):
        e = self.y - np.asarray(t).reshape(len(self.vocabulary), 1)
        dEdW1 = np.dot(self.h, e.T)
        X = np.array(x).reshape(len(self.vocabulary), 1)
        dEdW = np.dot(X, np.dot(self.W1, e).T)
        self.W1 = self.W1 - self.alpha * dEdW1
        self.W = self.W - self.alpha * dEdW

    def calculate_loss(self, word_context):
        C = 0
        for word_index in range(len(self.vocabulary)):
            if word_context[word_index]:
                self.loss -= self.u[word_index][0]
                C += 1
        self.loss += C * np.log(np.sum(np.exp(self.u)))

    def train(self, epochs):
        for epoch in range(1, epochs):
            self.loss = 0
            for word_ohe, word_context in zip(self.X_train, self.y_train):
                self.forward_propagation(word_ohe)
                self.backward_propagation(word_ohe, word_context)
                self.calculate_loss(word_context)
            if epoch % 5 == 0:
                print("epoch ", epoch, " loss = ", self.loss)
            self.alpha *= 1 / (1 + self.alpha * epoch)

    def predict(self, target_word, number_of_similar_words):
        assert target_word in self.vocabulary, 'Word not found in dictionary'
        word_index = self.words_indices[target_word]
        prediction = self.forward_propagation(one_hot_encode(word_index, self.vocabulary))
        output = dict()
        for i in range(len(self.vocabulary)):
            output[i] = prediction[i][0]
        similar_words = []
        sorted_words = sorted(output.items(), key=lambda x: x[1], reverse=True)
        # print(sorted_words)

        for word, value in sorted_words:
            similar_words.append(self.vocabulary[word])
            number_of_similar_words -= 1
            if number_of_similar_words == 0:
                break
        return similar_words


def one_hot_encode(word_index, vocabulary):
    X = [0 for i in range(len(vocabulary))]
    X[word_index] = 1
    return X


def read_file(filepath: str):
    with open(filepath) as file:
        filtered_file = filter(lambda x: x != "", file.read().split("\n"))
        return list(filtered_file)


def preprocess(corpus):
    word_tokenizer = re.compile("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+")
    stop_words = open('english_stopwords.txt').read().split("\n")

    preprocessed_text_sentences = []
    sentences = corpus.split(".")
    for sentence in sentences:
        sentence = word_tokenizer.findall(sentence)
        sentence = filter(lambda word: word not in stop_words, sentence)
        sentence = map(lambda word: word.lower(), sentence)
        sentence = list(sentence)
        preprocessed_text_sentences.append(sentence)
    return preprocessed_text_sentences


def get_training_data(preprocessed_text_sentences):
    occurrences = {}
    for sentence in preprocessed_text_sentences:
        for word in sentence:
            if word not in occurrences:
                occurrences[word] = 1
            else:
                occurrences[word] += 1
    occurrences = sorted(list(occurrences.keys()))

    words_indices = OrderedDict()
    for i in range(len(occurrences)):
        words_indices[occurrences[i]] = i
    vocabulary_length = len(words_indices)

    window_size = 2
    X = []
    y = []

    for sentence in preprocessed_text_sentences:
        for center_word_index in range(len(sentence)):
            center_word_one_hot = [0 for i in range(vocabulary_length)]
            outer_word_one_hot = [0 for i in range(vocabulary_length)]

            center_word_one_hot[words_indices[sentence[center_word_index]]] = 1
            for outer_word_index in range(center_word_index - window_size, center_word_index + window_size + 1):
                if 0 <= outer_word_index < len(sentence) and center_word_index != outer_word_index:
                    outer_word_one_hot[words_indices[sentence[outer_word_index]]] = 1

            X.append(center_word_one_hot)
            y.append(outer_word_one_hot)

    return X, y, words_indices


def tsne_plot(model):
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)
        print(model[word])
        print(('*******'))
        print(word)
        break
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
        print(x,y)

    plt.figure(figsize=(8, 8))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    #plt.show()


with open('val.txt') as text:
    corpus = text.read()
    preprocessed_text_sentences = preprocess(corpus)

    X, y,words_indices= get_training_data(preprocessed_text_sentences)
    NN = NeuralNetwork(X, y,words_indices)

    NN.train(100)
    similar_words = NN.predict("cat", 4)
    print(similar_words)

    model = word2vec.Word2Vec(preprocessed_text_sentences, size=10, window=2, min_count=1, workers=4, iter=200,
                              seed=100, alpha=0.05)

    tsne_plot(model)
