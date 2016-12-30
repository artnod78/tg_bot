# -*- coding: UTF-8 -*-
from TgLib import TgBot

token = '<token>'
white_list = ['<user>',]

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

def afficher_ligne(msg, resp, cmd):
	if resp.isOk():
		print("{} - {} - {} - {}".format(
			msg.get_Date(), 
			msg.get_MessageId(), 
			resp.get_UserName(), 
			cmd['cmd']+' '+cmd['param']
			)
		)
	else:
		print('{} - {} - ERROR {} - {}'.format(
			msg.get_Date(), 
			msg.get_MessageId(), 
			resp.get_ErrCode(),
			resp.get_Error()
			)
		)
	
def main():
	bot = TgBot(token, white_list)
	while(1):
		for msg in bot.get_MessageWithCommand():
			for cmd in msg.get_Command():
				if cmd['cmd'] in command_list:
					resp = bot.reply_Message(msg, reply[cmd['cmd']])
					afficher_ligne(msg, resp, cmd)
			bot.clear_Message(msg)

if __name__ == '__main__':
	main()