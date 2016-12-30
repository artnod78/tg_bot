# -*- coding: UTF-8 -*-
from TgLib import TgFiler

token = '<token>'
white_list = ['<user>',]
home_dir = r'<path>'

def afficher_ligne(resp):
	msg = resp['msg']
	cmd = resp['cmd']
	resp = resp['resp']
	if not resp == None:
		if resp.isOk():
			if type(cmd) != str:
				cmd = cmd['cmd']+' '+cmd['param']
			print("{} - {} - {} - {}".format(
				msg.get_Date(), 
				msg.get_MessageId(), 
				resp.get_UserName(), 
				cmd
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
	else:
		print("{} - {} - {} - {}".format(
			msg.get_Date(), 
			msg.get_MessageId(), 
			msg.get_ChatName(), 
			cmd['cmd']+' '+cmd['param']
			)
		)
	
def main():
	filserver = TgFiler(token, white_list, home_dir)
	while(1):
		response = filserver.run()
		for resp in response:
			afficher_ligne(resp)

if __name__ == '__main__':
	main()