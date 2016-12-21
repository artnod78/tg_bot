from TgLib import TgBot, TgMsg

command_list = ['start', 'help']

unknow_text ="""Désolé je ne comprends pas la demande.
Tu peux essayer /help pour obtenir de l'aide
"""

start_text ="""Bienvenue
Je suis un super bot stupide
Tu peux essayer /help pour obtenir de l'aide
"""

help_text ="""Bienvenue
Voici la liste des commandes disponible:
/help - Get help
"""
reply = {'null': unknow_text, 'help': help_text, 'start':start_text}

def afficher_ligne(msg, txt):
	print("{} - {} - {} - {} - {}".format(
		msg.get_Date(), 
		msg.get_UpdateId(), 
		msg.get_Username(), 
		msg.get_ChatId(), 
		txt
		))

def main():
	# on initialise le bot
	bot = TgBot("<token>")
	while(1):
		# recupere la liste de tout les messages avec des commandes
		msg_list = bot.get_MessageWithCommand()
		# traitement pour chaque message recupere
		for message in msg_list:
			# on initialise le message
			msg = TgMsg(message)
			# pour chaque commande
			for cmd in msg.get_Command():
				# si la commande existe
				if cmd in command_list:
					# on répond à la commande
					bot.reply_Message(msg, reply[cmd])
					# on affiche une ligne pour faire joli
					afficher_ligne(msg, cmd)
				# sinon
				else:
					# on repond un message basique
					bot.reply_Message(msg, reply['null'])
			# on efface le message
			bot.clear_Message(msg)

if __name__ == '__main__':
	main()
