import xgboost as xgb
import nltk
import pandas as pd
import numpy as np
from scipy import spatial
from sklearn import metrics
from nltk.stem import PorterStemmer
import gensim.models.keyedvectors as word2vec
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import Variables

class W2VIntentClassification:
    def load_faq_csv(file_name):
        data = pd.read_csv(file_name)
        return data

    # Create a model of word2vec using the gensim library
    def load_word2vec(path):
        mod = word2vec.KeyedVectors.load_word2vec_format(path, binary=True,)
        return mod

    # Now we converting the vector of word(Number) to its actual word
    def convertVector_to_word(model):
        index2word_set = set(model.wv.index2word)
        return index2word_set

    # Remove stop words like "I,this,that,these,and,the etc."
    def remove_stopwords(words):
        #nltk.download('stopwords')
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
        lower_case_words = W2VIntentClassification.lowercase(words)
        stop_words_removed =W2VIntentClassification.remove_stopwords(lower_case_words)
        # stemmed_words=app.stem(stop_words_removed)
        return stop_words_removed

    # here we will define the calculation of average word2vec for a sentence
    def average_word2vec_sentence(sentences, model, num_features, index2word_set):
        l1=[]
        for sent in sentences:
            cleaned_words = W2VIntentClassification.clean_text(sent)
            feature_vector = np.zeros((num_features,), dtype='float32')
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
    def average_word2vec_sentence1(sentence, model, num_features, index2word_set):
        cleaned_words = W2VIntentClassification.clean_text(sentence)
        feature_vector = np.zeros((num_features,), dtype='float32')
        n_words = 0
        for word in cleaned_words:
            if word in Variables.index2word_set:
                n_words += 1
                feature_vector = np.add(feature_vector,Variables.W2V_model[word])
            if (n_words > 0):
                feature_vector = np.divide(feature_vector, n_words)

        return feature_vector

    #split the data into train and test
    def split_data(data):
        X_train,X_test,y_train,y_test=train_test_split(data['Query'],data['Label'],random_state=42,test_size=0.5,shuffle=True)
        return X_train,X_test,y_train,y_test

    def Logistic_Regression(X_train_tvf ,X_test_tvf,y_train,y_test):
        estimator=LogisticRegression()
        param_grid={'C':[0.01,0.05,0.1,0.5,1,5,10],'penalty':['l1','l2']}
        optimizer=GridSearchCV(estimator,param_grid,cv=10)
        optimizer.fit(X_train_tvf,y_train)
        predict=optimizer.best_estimator_.predict(X_test_tvf)
        return metrics.accuracy_score(y_test,predict),optimizer

    def XG_Boost(X_train_tvf ,X_test_tvf,y_train,y_test):
        model = xgb.XGBClassifier(max_depth=7, n_estimators=200, colsample_bytree=0.8,
                                  subsample=0.8, nthread=10, learning_rate=0.1)
        model.fit(X_train_tvf, y_train)
        predictions = model.predict(X_test_tvf)
        accuracy=metrics.accuracy_score(y_test, predictions)
        return accuracy,model

    def load_w2vmodel(self):

        data = W2VIntentClassification.load_faq_csv('/home/manjunathh/chatbot/UserQueries.csv')
        print("load word2vec")
        Variables.W2V_model= W2VIntentClassification.load_word2vec('/home/manjunathh/chatbot/GoogleNews-vectors-negative300.bin.gz')
        print("word2vec loaded")
        Variables.index2word_set = W2VIntentClassification.convertVector_to_word(Variables.W2V_model)
        X_train, X_test, y_train, y_test = W2VIntentClassification.split_data(data)
        X_train_w2c = W2VIntentClassification.average_word2vec_sentence(X_train, Variables.W2V_model, 300,Variables.index2word_set)
        X_test_w2c = W2VIntentClassification.average_word2vec_sentence(X_test, Variables.W2V_model, 300, Variables.index2word_set)
        accuracy, model_LG = W2VIntentClassification.Logistic_Regression(X_train_w2c, X_test_w2c, y_train, y_test)
        #accuracy, model_LG = W2VIntentClassification.XG_Boost(X_train_w2c, X_test_w2c, y_train, y_test)
        print("Accuracy of word2vecmodel:",accuracy*100)
        return model_LG


    def final(text):
        if Variables.W2V_model==None:
            print("In final if of W2VIntent")
            Variables.model_LG=W2VIntentClassification.load_w2vmodel(1)
            query_w2c = W2VIntentClassification.average_word2vec_sentence1(text, Variables.W2V_model, 300,
                                                                           Variables.index2word_set)
            label1 = Variables.model_LG.best_estimator_.predict([query_w2c])
            label1_prob = Variables.model_LG.best_estimator_.predict_proba([query_w2c])
            # label1 = Variables.model_LG.predict(query_w2c)
            # label1_prob = Variables.model_LG.predict_proba(query_w2c)

            print("Label Prob:", label1_prob)
        else:
            print("In final else of W2VIntent")
            query_w2c =W2VIntentClassification.average_word2vec_sentence1(text,Variables.W2V_model,300,
                                                                          Variables.index2word_set)
            label1 = Variables.model_LG.best_estimator_.predict([query_w2c])
            label1_prob=Variables.model_LG.best_estimator_.predict_proba([query_w2c])
            # label1 = Variables.model_LG.predict(query_w2c)
            # label1_prob = Variables.model_LG.predict_proba(query_w2c)

            print("Label Prob:",label1_prob)
        return label1
    #
    # if __name__ == '__main__':
    #     data = load_faq_csv('/home/manjunathh/chatbot/UserQueries.csv')
    #     print("load word2vec")
    #     model=load_word2vec('/home/manjunathh/chatbot/GoogleNews-vectors-negative300.bin.gz')
    #     print("word2vec loaded")
    #     index2word_set=convertVector_to_word(model)
    #     X_train, X_test, y_train, y_test = split_data(data)
    #     X_train_w2c=average_word2vec_sentence(X_train,model,300, index2word_set)
    #     X_test_w2c = average_word2vec_sentence(X_test,model,300, index2word_set)
    #     print(len(X_train_w2c[0]))
    #     print(len(X_test_w2c[0]))
    #     print(len(X_train_w2c))
    #     print(len(X_test_w2c))
    #
    #     accuracy, model_1 = XG_Boost(X_train_w2c, X_test_w2c, y_train, y_test)
    #     print(accuracy)


        # while(True):
        #     query = input()
        #     query_w2c =average_word2vec_sentence1(query,model,300, index2word_set)
        #     print(len(query_w2c))
        #     label1 = model_1.best_estimator_.predict([query_w2c])
        #     print("=======================================================",label1)

