import nltk
import pandas as pd
import numpy as np
from scipy import spatial
from nltk.stem import PorterStemmer
import gensim.models.keyedvectors as word2vec
from nltk.corpus import stopwords
# import Levenshtein
from fuzzywuzzy import fuzz
import logging
import Variables

class FAQConversation:

    def load_faq_csv(file_name):
        data = pd.read_csv(file_name)
        return data
    # # Create a model of word2vec using the gensim library
    # def load_word2vec(path):
    #     mod = word2vec.KeyedVectors.load_word2vec_format(path, binary=True)
    #     return mod
    #
    # # Now we converting the vector of word(Number) to its actual word
    # def convertVector_to_word(model):
    #     index2word_set = set(model.wv.index2word)
    #     return index2word_set

    # Remove stop words like "I,this,that,these,and,the etc."
    def remove_stopwords(words):
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
    def average_word2vec_sentence(sentence):
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

    def word2vec_score(query, data):
        sim_word2vec = []
        for faq in data['Questions']:
            s1_afv = FAQConversation.average_word2vec_sentence(query)
            s2_afv = FAQConversation.average_word2vec_sentence(faq)
            score = 1 - spatial.distance.cosine(s1_afv, s2_afv)
            sim_word2vec.append(score)
            # print(query,"====",faq,"====",score)
        return sim_word2vec

    def fuzzy_wuzzy_score(query, data):
        sim_fuzzywuzzy = []
        for faq in data['Questions']:
            # ratio : compares the entire string similarity, in order
            ratio1 = fuzz.ratio(query, faq)
            # partial_ratio:compares partial string similarity
            ratio2 = fuzz.partial_ratio(query, faq)
            # token_sort_ratio:Ignores word order
            ratio3 = fuzz.token_sort_ratio(query, faq)
            # token_set_ratio , ignores duplicated words.It is similar with token sort ratio,but a little more flexible
            ratio4 = fuzz.token_set_ratio(query, faq)
            score = (ratio1 + ratio2 + ratio3 + ratio4) / (4 * 100)
            sim_fuzzywuzzy.append(score)
            # print(query,"====",faq,"====",score)
        return sim_fuzzywuzzy


    def bot_reply_avg_word2vec(query,data):
        score_word2vec = FAQConversation.word2vec_score(query, data)
        score_fuzzy_wuzzy = FAQConversation.fuzzy_wuzzy_score(query, data)
        data['Score'] = [sum(x) for x in zip(score_word2vec, score_fuzzy_wuzzy)]
        #print(data.loc[data['Score'].argmax(), ['Questions', 'Answers']])
        print("i am here")
        return data.loc[data['Score'].argmax(), ['Answers']].item()

    def final(query):
        data = FAQConversation.load_faq_csv('/home/manjunathh/chatbot/Faq.csv')
        # print("Loading Word2Vec")
        # model = app.load_word2vec('/home/manjunathh/chatbot/GoogleNews-vectors-negative300.bin.gz')
        # print("Word2vec Loaded")
        # index2word_set = app.convertVector_to_word(model)
        reply = FAQConversation.bot_reply_avg_word2vec(query, data)
        print(type(reply))
        return reply


# if __name__ == '__main__':
#     data = app.load_faq_csv('/home/manjunathh/chatbot/Faq.csv')
#     print("Loading Word2Vec")
#     model=app.load_word2vec('/home/manjunathh/chatbot/GoogleNews-vectors-negative300.bin.gz')
#     print("Word2vec Loaded")
#     index2word_set=app.convertVector_to_word(model)
#     while(True):
#         print("Enter a query:")
#         query = input()
#         print(data)
#         reply=app.Calculate_Score(query,data)
#