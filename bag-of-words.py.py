# print("hello")
# filename =
# file = open(filename, 'r')
# text = file.read()
# file.close()
# z = text.split()
# print(z)

# main motto is to convert it into feature vector
import nltk
# nltk.download()

# for filename in listdir(dir_pos):
#     if not filename.endswith(".txt"):
#         next
#     path = dir_pos + '/' + filename
#     doc = load_doc(path)
#     # print('Loaded %s' %filename)
# filename = 'txt_sentoken/neg/cv000_29416.txt'
# txt = load_doc(filename)
# tokens  = txt.split()
# # print(tokens[:50])
# re_punc = re.compile('[%s]' % re.escape(string.punctuation))      #punctuation skip re container
# tokens = [re_punc.sub('', w) for w in tokens]                     #substitute by nothing
# tokens = [word for word in tokens if word.isalpha()]
# stopWords = set(stopwords.words('english'))
# # print(stopWords)
# # print(tokens[:50])
# tokens = [word for word in tokens if word not in stopWords]      #remove the stopwords
# tokens = [word for word in tokens if len(word) > 1]
# filename = "txt_sentoken/pos/cv000_29590.txt"
# text = load_doc(filename)
# tokens = clean_doc(text)
# print(tokens)

# now let us clean the data and then convert it into feature vector


from os import listdir
from nltk.corpus import stopwords
import string
import re
from collections import Counter

def load_doc(filename):
    file = open(filename,'r')
    text = file.read()
    file.close()
    return text


#  so token contains all the cleaned text ready to represented

def clean_doc(doc):
    tokens = doc.split()
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))  # punctuation skip re container
    tokens = [re_punc.sub('', w) for w in tokens]  # substitute by nothing
    tokens = [word for word in tokens if word.isalpha()]
    stopWords = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stopWords]  # remove the stopwords
    tokens = [word for word in tokens if len(word) > 1]
    return tokens



def add_doc_to_vocab(filename, vocab):
    doc = load_doc(filename)
    tokens = clean_doc(doc)
    vocab.update(tokens)        #similar to multi-set

def process_doc(directory, vocab):
    for filename in listdir(directory):
        if not filename.endswith(".txt"):
            next
        path = directory + '/' + filename
        add_doc_to_vocab(path, vocab)

vocab = Counter()
dir_pos = "txt_sentoken/pos"
dir_neg = "txt_sentoken/neg"

# process the doc and develop the vocabulary
process_doc(dir_pos, vocab)
process_doc(dir_neg, vocab)

#  print the length of the vocab
print(len(vocab))
print(vocab.most_common(50))

min_occurence = 5
tokens = [word for word, count in vocab.items() if count > min_occurence]
print(len(tokens))

def save_list(lines, filename):
    data  = '\n'.join(lines)
    file = open(filename, 'w')
    file.write(data)
    file.close()

save_list(tokens, 'vocab.txt')

# load vocabulary
vocab_filename = 'vocab.txt'
vocab = load_doc(vocab_filename)
vocab = vocab.split()
vocab = set(vocab)
# print(vocab)

def doc_to_line(filename, vocab):
    doc = load_doc(filename)
    tokens = clean_doc(doc)
    tokens = [word for word in tokens if word in vocab]
    return " ".join(tokens)

def process_docs(directory, vocab):
    lines = []
    for filename in listdir(directory):
        if not filename.endswith(".txt"):
            next
        path = directory + '/' + filename
        line = doc_to_line(path, vocab)
        lines.append(line)
    return lines

negative = process_docs(dir_neg, vocab)
save_list(negative, 'negative.txt')
positive = process_docs(dir_pos, vocab)
save_list(positive, 'positive.txt')




