from TgBot import TgBot

command_list = ['help','date']

unknow_text ="""
Désolé je ne comprends pas la demande
"""

help_text ="""
Bienvenue
Voici la liste des commandes disponible:
/help - Get help
"""
reply = {'null': unknow_text, 'help': help_text}

	
def main():
	# on initialise le bot
	bot = TgBot("<token>")
	while(1):
		# recupere la liste de tout les messages
		new_msg = bot.getUpdates_messages()
		# traitement pour chaque message recupere
		for msg in new_msg:
			# extraction des commandes
			cmds = bot.getCommand(msg)
			# pour chaque commande
			for cmd in cmds:
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
			date = bot.getDate(msg)
			text = bot.getText(msg)
			print("{} - {} - {} - {} - {}".format(date, msg['update_id'], msg['message']['from']['username'], msg['message']['chat']['id'], text))

if __name__ == '__main__':
	main()