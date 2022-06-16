import gensim, logging, os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from cope_dataset import get_unrepeat_txt
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
import nltk
from gensim.models import word2vec
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sentence_transformers import SentenceTransformer


def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def tsne_plot(tokens,labels):

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
    plt.savefig('embedding_map.png')

def train(str_en_text):
    tokenized_sent = []

    for s in str_en_text:
        tokenized_sent.append(word_tokenize(s.lower()))
    tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_sent)]

    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    sentence_embeddings = sbert_model.encode(str_en_text) #  得到了每一个句子的向量

    tsne_plot(sentence_embeddings[:88],str_en_text[:88])
    # 对比句子之间的相似度
    #query = "Will the cat tower topple over easily？My cat is about 7-8 pounds."
    # query_vec = sbert_model.encode([query])[0]
    # for sent in str_en_text:
    #     sim = cosine(query_vec, sbert_model.encode([sent])[0])
    #     #print("Sentence = ", sent, "; similarity = ", sim)
    #     if float(sim)>0.8:
    #         break





if __name__ == '__main__':
    json_path = '/cloud/cloud_disk/users/huh/dataset/nlp_dataset/question_dataset/ori/en_ch_cattree_personality.json'
    str_en_text = get_unrepeat_txt()
    train(str_en_text)
