# -*- coding: UTF-8 -*-
from TgLib import TgBot, TgMsg

token = "<token>"
white_list = ['<username>',]

command_list = ['start', 'help']

start_text ="""Bienvenue
Je suis un super bot stupide
Tu peux essayer /help pour obtenir de l'aide
"""

help_text ="""Voici la liste des commandes disponible:
/start - Start bot
/help - Get help
"""
reply = {'start':start_text , 'help': help_text}

def afficher_ligne(msg, txt):
	print("{} - {} - {} - {} - {}".format(
		msg.get_Date(), 
		msg.get_UpdateId(), 
		msg.get_Username(), 
		msg.get_ChatId(), 
		txt
		)
	)

def main():
	bot = TgBot(token, white_list)
	while(1):
		for msg in bot.get_MessageWithCommand():
			for cmd in msg.get_Command():
				if cmd['cmd'] in command_list:
					bot.reply_Message(msg, reply[cmd['cmd']])
					afficher_ligne(msg, cmd)
			bot.clear_Message(msg)

if __name__ == '__main__':
	main()