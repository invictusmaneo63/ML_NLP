import unicodedata
import re
import random
import numpy as np
import word_embedding as embed

SOS_token, EOS_token = 0, 1
MAX_LENGTH = 15

class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {'SOS': 0, 'EOS': 1} # vocabulary
        self.word2count = {}
        self.index2word = {0: 'SOS', 1: 'EOS'}
        self.n_words = 2 # SOS, EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)
    
    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

def unicodeToAscii(s): 
    # Turn a Unicode string to plain ASCII
    # refer to https://stackoverflow.com/a/518232/2809427
    return ''.join( c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normalizeString(s):
    # lowercase, trim and remove non-letter characters
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    
    return s

def readLangs(lang1, lang2, reverse=False):
    print('Reading lines..')
    # Read the file and split into lines
    lines = open('../data/%s-%s.txt' % (lang1, lang2), encoding='utf-8').read().strip().split('\n')

    # Split every line into pairs and normalize
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]

    # Reverse pairs, make Lang instances
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)

    return input_lang, output_lang, pairs

def filterPair(p):
    return len(p[0].split(' ')) < MAX_LENGTH and len(p[1].split(' ')) < MAX_LENGTH

def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

def prepareData(lang1, lang2, reverse=False):
    input_lang, output_lang, pairs = readLangs(lang1, lang2, reverse)
    print('Read {} sentence pairs'.format(len(pairs)))

    pairs = filterPairs(pairs)    
    print('Trimmed to {} sentence pairs'.format(len(pairs)))

    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    print('Counted words: {}- {}\t{} - {}'.format(input_lang.name, input_lang.n_words,
                                                  output_lang.name, output_lang.n_words))
    return input_lang, output_lang, pairs

def prepareEmbMatrix(trained_vector_paths, vector_size, input_lang, output_lang, reverse=False):
    if reverse:
        input_emb_matrix = embed.get_embedding_matrix(input_lang.word2index,
                                                    trained_vector_paths[1], vector_size)
        output_emb_matrix = embed.get_embedding_matrix(output_lang.word2index,
                                                    trained_vector_paths[0], vector_size)
    else:
        input_emb_matrix = embed.get_embedding_matrix(input_lang.word2index,
                                                    trained_vector_paths[0], vector_size)
        output_emb_matrix = embed.get_embedding_matrix(output_lang.word2index,
                                                    trained_vector_paths[1], vector_size)

    SOS_token_vec = embed.initSpecialToken(vector_size, 0) # SOS
    EOS_token_vec = embed.initSpecialToken(vector_size, 0) # EOS
    for idx, tvec in enumerate((SOS_token_vec, EOS_token_vec)):
        input_emb_matrix[idx] = tvec
        output_emb_matrix[idx] = tvec

    return input_emb_matrix, output_emb_matrix

if __name__ == "__main__":
    '''
    The full process for preparing the data is:
        1. Read text file and split into lines, split lines into pairs
        2. Normalize text, filter by length and content
        3. Make word lists from sentences in pairs
    '''
    input_lang, output_lang, pairs = prepareData('eng', 'fra', True)
    print(random.choice(pairs))
    
    trained_vector_paths = ('cc.en.300.vec', 'cc.fr.300.vec')
    input_emb_matrix, output_emb_matrix = prepareEmbMatrix(trained_vector_paths, 300, input_lang, output_lang, True)
    print('Embedding-matrix shape: {}, {}'.format(input_emb_matrix.shape, output_emb_matrix.shape))
    
    np.save('input_emb_matrix', input_emb_matrix)
    np.save('output_emb_matrix', output_emb_matrix)