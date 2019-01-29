
import pandas as pd
from flask import Flask, request
from pymessenger import Bot
import requests
import datetime
import random
import Variables,IntentClassification,HolidayConversation,LeaveConversation1,Conversation,W2VIntentClassification,FAQConversation
from LeaveConversation1 import LeaveConversation1

app = Flask("Eximius HR Chatbot")

FB_ACCESS_TOKEN = "EAAD8jL36JM8BANPjrBeOjUeyODZAZAm9G9Tz8dWFEEN0PXn04FC9XscRVbv1VKKpPvi76DcXOZC5XUBvIYtJ7mp19pPHSBuZAV2bnZA3qPzCcS1C4HlJkMFydxpmjSNEHjL2WcTUK22lp6owWumwjnZCbDCx0IClbjMG7ZCQwZBkR9UvJKdYuZBN9"
bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hello"


@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200

def response(label,text):
	if label==Conversation.Conversations.labels[0]:
		print("in ",Conversation.Conversations.labels[0])
		Variables.label=None
		return HolidayConversation.HolidayConversation.main(text)
	elif label==Conversation.Conversations.labels[1]:
		print("in ", Conversation.Conversations.labels[1])
		return LeaveConversation1.main(text)
	elif label==Conversation.Conversations.labels[2]:
		print("in ", Conversation.Conversations.labels[2])
		 #print(3)
		Variables.label = None
		return Conversation.Conversations.Hi_Replay(1)
	elif label==Conversation.Conversations.labels[3]:
		print("in ", Conversation.Conversations.labels[3])
		Variables.label = None
		return random.choice(Conversation.Conversations.Thanks_replays)
	elif label==Conversation.Conversations.labels[4]:
		print("in ", Conversation.Conversations.labels[4])
		Variables.label = None
		return FAQConversation.FAQConversation.final(text)
		 #return "FAQ"
	else:
		Variables.label = None
		return "No intents Matched"

def get_bot_response(userText):
	if userText=="cancel":
		LeaveConversation1.flush(1)
		return Conversation.Conversations.boot_conversations[20]
	elif Variables.label==None:
		#Variables.label=IntentClassification.intent_classification.final(userText)
		print("here")
		Variables.label = W2VIntentClassification.W2VIntentClassification.final(userText)
	r=response(Variables.label,userText)
	if isinstance(r,pd.DataFrame):
		#return Conversation.Conversations.boot_conversations[12]+"\n"+r.to_html()
		return Conversation.Conversations.boot_conversations[12]+"\n\n"+r.to_string()
	else:
		return str(r)



@app.route('/', methods=['POST'])
def webhook():
	print("in web hook")
	output = request.get_json()
	for event in output['entry']:
		messaging = event['messaging']
		for message in messaging:
			if message.get('message'):
				# Facebook Messenger ID for user so we know where to send response back to
				recipient_id = message['sender']['id']
				if message['message'].get('text'):
					query = message['message']['text']
					print("query:", query)
					reply=get_bot_response(query)
					print(reply)
					bot.send_text_message(recipient_id, reply)

	return "ok", 200


@app.before_first_request
def before_first_request():
	print('########### Restarted,')
	if Variables.W2V_model == None:
		print("started loading")
		Variables.model_LG = W2VIntentClassification.W2VIntentClassification.load_w2vmodel(1)
		print("W2v loading finished555555555555")
	else:
		print("Word2Vec model already loaded")

# @app.before_request
# def before_request():
# 	print('########### Restarted,')
# 	# if Variables.W2V_model == None:
# 	# 	print("started loading")
# 	# 	Variables.model_LG = W2VIntentClassification.W2VIntentClassification.load_w2vmodel(1)
# 	# 	print("W2v loading finished555555555555")
# 	# else:
# 	# 	print("Word2Vec model already loaded")


if __name__ == "__main__":
	print("in main of FBapp")
	app.run(port=8000,debug=True, use_reloader=True)