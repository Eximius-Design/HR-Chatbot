import pandas as pd
import gensim.models.keyedvectors as word2vec
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np
from sklearn.model_selection import train_test_split
import Variables


class FAQConversation:
    def read_csv(file_name):
        data = pd.read_csv(file_name)
        return data

    # Create a model of word2vec using the gensim library
    def load_word2vec(path):
        mod = word2vec.KeyedVectors.load_word2vec_format(path, binary=True, )
        return mod

    # Now we converting the vector of word(Number) to its actual word
    def convertVector_to_word(model):
        index2word_set = set(model.wv.index2word)
        return index2word_set

    # Now we converting the vector of word(Number) to its actual word
    def convertVector_to_word(model):
        index2word_set = set(model.wv.index2word)
        return index2word_set

    # Remove stop words like "I,this,that,these,and,the etc."
    def remove_stopwords(words):
        # nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        # return " ".join(w for w in words if w not in stop_words)
        return [w for w in words if w not in stop_words]

    def lowercase(words):
        # return " ".join(w.lower() for w in words)
        return [w.lower() for w in words]

    # stemming of word
    def stem(words):
        ps = PorterStemmer()
        # return " ".join(ps.stem(w) for w in words)
        return [ps.stem(w) for w in words]

    def clean_text(sentence):
        words = str(sentence).split()
        lower_case_words = FAQConversation.lowercase(words)
        stop_words_removed = FAQConversation.remove_stopwords(lower_case_words)
        # stemmed_words=app.stem(stop_words_removed)
        return stop_words_removed

    # here we will define the calculation of average word2vec for a sentence
    def average_word2vec_sentence(sentences):
        l1 = []
        for sent in sentences:
            cleaned_words = FAQConversation.clean_text(sent)
            feature_vector = np.zeros((300,), dtype='float32')
            n_words = 0
            for word in cleaned_words:
                if word in Variables.index2word_set:
                    n_words += 1
                    feature_vector = np.add(feature_vector, Variables.W2V_model[word])
                if (n_words > 0):
                    feature_vector = np.divide(feature_vector, n_words)

            l1.append(feature_vector)
        return l1
        # here we will define the calculation of average word2vec for a sentence

    # here we will define the calculation of average word2vec for a sentence
    def average_word2vec_sentence1(sentence):
        cleaned_words = FAQConversation.clean_text(sentence)
        feature_vector = np.zeros((300,), dtype='float32')
        n_words = 0
        for word in cleaned_words:
            if word in Variables.index2word_set:
                n_words += 1
                feature_vector = np.add(feature_vector, Variables.W2V_model[word])
            if (n_words > 0):
                feature_vector = np.divide(feature_vector, n_words)

        return feature_vector


if __name__ == '__main__':
    data = FAQConversation.read_csv('/home/manjunathh/chatbot/Faq.csv')
    print("load word2vec")
    Variables.W2V_model = FAQConversation.load_word2vec(
        '/home/manjunathh/chatbot/GoogleNews-vectors-negative300.bin.gz')
    print("word2vec loaded")
    Variables.index2word_set = FAQConversation.convertVector_to_word(Variables.W2V_model)
    FAQ_Word2Vec = FAQConversation.average_word2vec_sentence(data['Questions'])
    while (True):
        query = input()
        print(query)
        Query_Word2Vec = FAQConversation.average_word2vec_sentence1(query)



