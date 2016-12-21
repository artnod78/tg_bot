import requests, json, datetime

class TgMsg:
	"""Classe définissant un message de Telegram caractérisée par :
	- son message"""

	msg = []

	def __init__(self, msg):
		self.msg = msg

	def have_Text(self):
		if('text' in msg['message']):
			return True
		return False

	def have_Command(self):
		if('entities' in self.msg['message']):
			for cmd in self.msg['message']['entities']:
				if(cmd['type'] == 'bot_command'):
					return True
		return False

	def get_Date(self):
		return datetime.datetime.fromtimestamp(self.msg['message']['date'])
	
	def get_Text(self):
		if('text' in self.msg['message']):
			return self.msg['message']['text']
		return ""
	
	def get_Command(self):
		cmd_list = []
		if(self.have_Command()):
			for cmd in self.msg['message']['entities']:
				if(cmd['type'] == 'bot_command'):
					start_cmd = cmd['offset'] +1
					stop_cmd = cmd['offset'] + cmd['length']
					commande = self.get_Text()[start_cmd:stop_cmd]
					cmd_list.append(commande)
		return cmd_list

	def get_UpdateId(self):
		return self.msg['update_id']
		
	def get_Username(self):
		return self.msg['message']['from']['username']
		
	def get_ChatId(self):
		return self.msg['message']['chat']['id']

class TgBot:
	"""Classe définissant un bot pour Telegram caractérisée par :
	- son token"""

	URL = "not set"

	def __init__(self, token):
		self.token = token
		self.URL = "https://api.telegram.org/bot{}/".format(token)

	def get_Updates(self, param = {}):
		response = requests.post(
			url = self.URL + "getUpdates",
			data= param
		)
		js = json.loads(response.content.decode("utf8"))
		return js

	def get_MessageWithCommand(self):
		msg_list = []
		update_list = self.get_Updates()
		if(update_list['ok']):
			for message in update_list['result']:
				msg = TgMsg(message)
				if(msg.have_Command()):
					msg_list.append(message)
		return msg_list
		
	def reply_Message(self, msg, text):
		response = requests.post(
			url = self.URL + "sendMessage",
			data={'reply_to_message_id': msg['message']['message_id'], 'chat_id': msg['message']['chat']['id'], 'text': text}
		)
		
	def clear_Message(self, msg):
		data = {'offset':msg['update_id']+1}
		null = self.get_Updates(data)
