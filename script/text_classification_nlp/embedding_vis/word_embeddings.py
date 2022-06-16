import re
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from typing import List


def one_hot_encode(string: str, strings: List[str]):
    one_hot_encoded = map(lambda s: 1 if s == string else 0, strings)
    return list(one_hot_encoded)


word_tokenizer = re.compile("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+")
with open('tweets_subset.txt') as file:
    ar = np.array([])
    for row in file:
        words = word_tokenizer.findall(row)
        words = list(map(lambda word: word.lower(), words))
        ar = np.concatenate([ar, words])

print(len(ar))

with open('english_stopwords.txt') as file:
    for stopword in file:
        stopword = stopword.rstrip('\n')
        ar = np.delete(ar, np.argwhere(ar == stopword))

print(len(ar))


print(ar)
# integer encode
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(ar)
print(integer_encoded)

# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
print(integer_encoded)

onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
print(onehot_encoded)
print(onehot_encoded.T)
