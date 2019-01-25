import pandas as pd
from flask import Flask, request
from pymessenger import Bot
import requests
import Variables,IntentClassification,HolidayConversation,LeaveConversation1,Conversation
app = Flask("My echo bot")

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
    print(text)
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

def get_bot_response(userText):
	if userText=="cancel":
	   return Conversation.Conversations.boot_conversations[20]
	elif Variables.label==None:
	   Variables.label=IntentClassification.intent_classification.final(userText)
	   print("here")
		#Variables.label = W2VIntentClassification.W2VIntentClassification.final(userText)

	r=response(Variables.label,userText)
	if isinstance(r,pd.DataFrame):
		#print(r.to_html())
		#return Conversation.Conversations.boot_conversations[12]+"\n"+r.to_html()
		return Conversation.Conversations.boot_conversations[12]+"\n\n"+r.to_string()

		#return s
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

# @app.route('/', methods=['POST'])
# def webhook():
# 	print("in web hook")
# 	#print(request.data)
# 	data = request.get_json()
# 	#flush()
# 	if data['object'] == "page":
# 		entries = data['entry']
# 		print(data)
# 		for entry in entries:
# 			messaging = entry['messaging']
#
# 			for messaging_event in messaging:
#
# 				sender_id = messaging_event['sender']['id']
# 				recipient_id = messaging_event['recipient']['id']
#
# 				if messaging_event.get('message'):
# 					# HANDLE NORMAL MESSAGES HERE
# 					if messaging_event['message'].get('text'):
# 						# HANDLE TEXT MESSAGES
# 						query = messaging_event['message']['text']
# 						#query="i want leave"
# 						# ECHO THE RECEIVED MESSAGE
# 						# reply=get_bot_response(query)
# 						print("query:",query)
# 						#print("reply:",reply)
# 						# bot.send_text_message(sender_id, reply)
# 						bot.send_text_message(sender_id, "hi_")
# 	return "ok", 200

if __name__ == "__main__":
	app.run(port=8000, use_reloader = True)
