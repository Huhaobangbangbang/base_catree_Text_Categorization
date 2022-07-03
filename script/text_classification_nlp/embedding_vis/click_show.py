"""
 -*- coding: utf-8 -*-
 author： Hao Hu
 @date   2022/6/30 7:16 PM
"""
import gensim, logging, os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from cope_dataset import get_unrepeat_txt
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sentence_transformers import SentenceTransformer



def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def click_show():
    """定义一个点击事件，一点击就显示对应的句子"""

def tsne_plot(tokens, labels):
    """利用tsne生成图片"""
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)
    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
    plt.figure(figsize=(32, 32))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()



def train(str_en_text):
    tokenized_sent = []

    for s in str_en_text:
        tokenized_sent.append(word_tokenize(s.lower()))
    tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_sent)]
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    sentence_embeddings = sbert_model.encode(str_en_text)  # 得到了每一个句子的向量
    tsne_plot(sentence_embeddings[:88], str_en_text[:88])

if __name__ == '__main__':
    json_path = '/cloud/cloud_disk/users/huh/dataset/nlp_dataset/question_dataset/ori/en_ch_cattree_personality.json'
    str_en_text = get_unrepeat_txt()
    train(str_en_text[:100])





