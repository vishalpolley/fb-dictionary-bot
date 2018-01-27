from src import app
from pymessenger.bot import Bot
from flask import request, jsonify
from PyDictionary import PyDictionary as pydict
import os, json, requests, random

ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)

@app.route("/")
def home():
    return "Hasura Hello World"

# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/webhook", methods=['GET', 'POST'])
def receive_message():
	if request.method == 'GET':
		"""Before allowing people to message your bot, Facebook has implemented a verify token
		that confirms all requests that your bot receives came from Facebook.""" 
		token_sent = request.args.get("hub.verify_token")
		return verify_fb_token(token_sent)
	#if the request was not get, it must be POST and we can just proceed with sending a message back to user
	else:
		# get whatever message a user sent the bot
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				if message.get('message'):
					#Facebook Messenger ID for user so we know where to send response back to
					recipient_id = message['sender']['id']
					if message['message'].get('text'):
						response_sent_text = get_text_message(message['message'].get('text'))
						send_message(recipient_id, response_sent_text)
					#if user sends us a GIF, photo,video, or any other non-text item
					if message['message'].get('attachments'):
						response_sent_nontext = get_random_message()
						send_message(recipient_id, response_sent_nontext)
	return "Message Processed"


def verify_fb_token(token_sent):
	#take token sent by facebook and verify it matches the verify token you sent
	#if they match, allow the request, else return an error 
	if token_sent == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return 'Invalid verification token'

def get_text_message(message):
	s = '*' + message.title() + '* \n' 
	value = pydict.meaning(message)
	if value is None:
		return "Sorry, I couldn't find the meaning of this word"
	for k, v in value.items():
		s = s + '_' +str(k) + '_: '
		for x in v:
			s += str(x) + ', '
		s += '\n'
	return s[:-3]

#chooses a random message to send to the user
def get_random_message():
	sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
	# return selected item to the user
	return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
	#sends user the text message provided via input response parameter
	bot.send_text_message(recipient_id, response)
	return "success"

if __name__ == "__main__":
	app.run()