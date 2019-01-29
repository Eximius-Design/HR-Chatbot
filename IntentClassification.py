import pandas as pd
import xgboost as xgb
from nltk.corpus import stopwords
from sklearn import metrics
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

class intent_classification:
    def load_csv(file_name):
        data=pd.read_csv(file_name)
        return data

    def download_dependencies(self):
        stop_words=stopwords.words('english')

    #split the data into train and test
    def split_data(data):
        X_train,X_test,y_train,y_test=train_test_split(data['Query'],data['Label'],random_state=42,test_size=0.5,shuffle=True)
        return X_train,X_test,y_train,y_test

    def convert_text_vector(X_train,X_test):
        tvfidf=TfidfVectorizer(min_df=2,max_features=None,strip_accents='unicode',
                              analyzer='word',token_pattern=r'\w{1,}',ngram_range=(1,2),
                              use_idf=1,smooth_idf=1,sublinear_tf=1,stop_words='english')
        tvfidf.fit(list(X_train)+list(X_test))
        X_train_tvf=tvfidf.transform(X_train)
        X_test_tvf=tvfidf.transform(X_test)
        return X_train_tvf,X_test_tvf,tvfidf

    def convert_text_2Vector(tvfidf_model,query):
        tvf_query=tvfidf_model.transform(query)
        return tvf_query

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

    def Random_Forest(X_train_tvf, X_test_tvf, y_train, y_test):
        model = RandomForestClassifier(n_estimators=10000, max_depth=100)
        model.fit(X_train_tvf, y_train)
        predictions = model.predict(X_test_tvf)
        accuracy = metrics.accuracy_score(y_test, predictions)
        return accuracy, model

    def load_model(self):
        data = intent_classification.load_csv('/home/manjunathh/chatbot/UserQueries_new.csv')
        X_train, X_test, y_train, y_test = intent_classification.split_data(data)
        X_train_tvf, X_test_tvf, tvfidf_model = intent_classification.convert_text_vector(X_train, X_test)
        accuracy, model = intent_classification.Random_Forest(X_train_tvf, X_test_tvf, y_train, y_test)
        print("Accuracy of model is :",accuracy*100)
        return model,tvfidf_model

    def final(text):
        print("in final of Intent classification")
        model,tvfidf_model=intent_classification.load_model(2)
        tvf_query = intent_classification.convert_text_2Vector(tvfidf_model, [text])
        label = model.best_estimator_.predict(tvf_query)
        #label = model.predict(tvf_query)
        label_probability=model.predict_proba(tvf_query)
        print("Label Probability:",label_probability)
        print("label:",label)
        return label[0]
