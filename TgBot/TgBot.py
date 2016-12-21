import requests, json, datetime

class TgBot:
	"""Classe définissant un bot pour Telegram caractérisée par :
	- son token"""

	URL = "not set"

	def __init__(self, token):
		self.token = token
		self.URL = "https://api.telegram.org/bot{}/".format(token)

	def api_getUpdates(self, since = 0):
		response = requests.post(
			url = self.URL + "getUpdates",
			data={'offset':str(since)}
		)
		js = json.loads(response.content.decode("utf8"))
		return js
	
	def api_replyMessage(self, reply, text):
		response = requests.post(
			url = self.URL + "sendMessage",
			data={'reply_to_message_id': reply['message']['message_id'], 'chat_id': reply['message']['chat']['id'], 'text': text}
		)
		
	def api_clearUpdates(self, msg):
		null = self.api_getUpdates(msg['update_id']+1)

	def getUpdates_messages(self):
		updates_messages = []
		update_list = self.api_getUpdates()
		nb_msg = len(update_list['result'])
		if(update_list['ok']):
			if(nb_msg > 0):
				updates_messages = update_list['result']
		return updates_messages

	def get_url(self):
		return self.URL

	def getDate(self, msg):
		return datetime.datetime.fromtimestamp(msg['message']['date'])
	
	def getText(self, msg):
		if('text' in msg['message']):
			text = msg['message']['text']
		else:
			text = "null"
		return text
	
	def getCommand(self, msg):
		cmd_list = []
		if('entities' in msg['message']):
			entities = msg['message']['entities']
		else:
			entities = []
		for cmd in entities:
			if(cmd['type'] == 'bot_command'):
				start_cmd = cmd['offset'] +1
				stop_cmd = cmd['offset'] + cmd['length']
				commande = self.getText(msg)[start_cmd:stop_cmd]
				cmd_list.append(commande)
		return cmd_list