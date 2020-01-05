# print("hello")
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
sentences = [['this','is','the','first','sentence','for','word2vec'],
             ['this','is','the','second','sentence'],
             ['yet','another','sentence'],
             ['one','more','sentence'],
             ['and','the','final','sentence']]

model = Word2Vec(sentences,min_count= 1)
print(model)
X= model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)
# print(result)
# print(result[:,0])


# create a scatter plot for the show
plt.scatter(result[:, 0], result[:, 1])
# plt.show()
words = list(model.wv.vocab)
for i,word in enumerate(words):
    plt.annotate(word, xy=(result[i, 0], result[i, 1]))
plt.show()

# print(words)
# print(model['another'])
model.save('model.bin')
new_model = Word2Vec.load('model.bin')
print(new_model)