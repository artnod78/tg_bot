import requests, json, datetime

command_list = ['help','date']

unknow_text ="""
Désolé je ne comprends pas la demande
"""

help_text ="""
Bienvenue
Voici la liste des commandes disponible:
/help - Get help
"""
reply = {'null': unknow_text, 'help': help_text,}

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

def main():

	# on initialise le bot
	bot = TgBot("320922006:AAEPVhgGVKn4HZtB_zpCAIZXPFEeIhUEvXY")
	while(1):
	
		# recupere la liste de tout les messages
		new_msg = bot.getUpdates_messages()
		
		# traitement pour chaque message recupere
		for msg in new_msg:
		
			# extraction de la date d'envoi
			date = bot.getDate(msg)
			# extraction du champs text
			text = bot.getText(msg)
			# extraction des commandes
			cmds = bot.getCommand(msg)
			
			# pour chaque commande
			for cmd in cmds:
				print(cmd)
				# si la commande existe
				if cmd in command_list:
					# on répond à la commande
					bot.api_replyMessage(msg, reply[cmd])
				# sinon
				else:
					# on repond un message basique
					bot.api_replyMessage(msg, reply['null'])
					
			# on efface le message
			bot.api_clearUpdates(msg)
			
			# on affiche une ligne pour faire joli
			print("{} - {} - {} - {} - {}".format(date, msg['update_id'], msg['message']['from']['username'], msg['message']['chat']['id'], text))

if __name__ == '__main__':
	main()
