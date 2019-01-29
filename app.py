import pickle
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
import pandas as pd
import LeaveConversation1,HolidayConversation,IntentClassification
import Variables
import Conversation
import W2VIntentClassification
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


def intent_classify(text):
    df = pd.read_csv("/home/manjunathh/chatbot/UserQueries.csv")
    # Features and Labels
    X = df['Query']
    y = df['Label']

    # Extract Feature With CountVectorizer
    cv = CountVectorizer()
    X = cv.fit_transform(X)  # Fit the Data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
    # Naive Bayes Classifier
    from sklearn.naive_bayes import MultinomialNB

    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    clf.score(X_test, y_test)
    vect = cv.transform(text).toarray()
    my_prediction = clf.predict(vect)

    return my_prediction


def response(label,text):
    if label=="Holiday":
        print(1)
        Variables.label=None
        return HolidayConversation.HolidayConversation.main(text)
    elif label=="Leave":
        print(2)
        return LeaveConversation1.LeaveConversation1.main(text)
    else:
        print(3)
        #print(3)
        return 3

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    #label = intent_classify([userText])
    ##Here below we are using the two types of intent classifiers
    #1.IntentClassification.py uses Tfidf based vector
    #2.W2VIntentClassification.py uses word2vec based vectors(Takes 2:30 minutes to load the model)
    if Variables.label==None:
        Variables.label=IntentClassification.intent_classification.final(userText)
        print("here")
        #Variables.label = W2VIntentClassification.W2VIntentClassification.final(userText)
    #print(response(label, userText))
    #return label
    #print(label)

    r=response(Variables.label,userText)
    if isinstance(r,pd.DataFrame):
        #print(r.to_html())
        return Conversation.Conversations.boot_conversations[12]+r.to_html()
        #return r.to_string()
    else:
        return str(r)

if __name__ == "__main__":
    app.run(port=5000, use_reloader = True)
