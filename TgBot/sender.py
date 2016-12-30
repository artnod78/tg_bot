# -*- coding: UTF-8 -*-
import sys
from TgLib import TgSender

token = '<token>'
white_list = [] # laisser vide

user = sys.argv[1]
message = ' '.join(map(str, sys.argv[2:]))

def afficher_ligne(resp):
	if resp.isOk():
		print('{} - {} - {} - {}'.format(
			resp.get_Date(),
			resp.get_MessageId(),
			resp.get_UserName(),
			resp.get_Text()
			)
		)
	else:
		print('ERROR {} - {}'.format(
			resp.get_ErrCode(),
			resp.get_Error()
			)
		)

def main():
	sender = TgSender(token, white_list)
	resp = sender.send(user, message)
	afficher_ligne(resp)
	

if __name__ == '__main__':
	main()