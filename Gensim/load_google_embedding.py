
# checking if the model from file can be loaded
from gensim.models import Word2Vec
my_model =Word2Vec.load('model.bin')
print(list(my_model.wv.vocab))

# trying to load google embedding
from gensim.models import KeyedVectors
filename = 'GoogleNews-vectors-negative300.bin'
model = KeyedVectors.load_word2vec_format(filename, binary = True)
result = model.most_similar(positive=['woman','king'], negative=['man'], topn=1)
print(result)