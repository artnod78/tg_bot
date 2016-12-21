import requests, json, datetime

TOKEN = ""
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

unknow_text ="""
Désolé je ne comprends pas la demande
"""
help_text ="""
Bienvenue
Voici la liste des commandes disponible:
/help - Get help
"""

def get_updates(offset):
	response = requests.post(
		url = URL + "getUpdates",
		data={'offset':offset}
	)
	js = json.loads(response.content.decode("utf8"))
	return js

def repondre_message(msgId, chatId, text):
	response = requests.post(
	url = URL + "sendMessage",
	data={'reply_to_message_id':msgId, 'chat_id': chatId, 'text': text}
	)

def get_updates_messages():
	new_msg = []
	update_list = get_updates(0)
	nb_msg = len(update_list['result'])
	if(update_list['ok']):
		if(nb_msg > 0):
			for msg in update_list['result']:   
					update_id = msg['update_id']
					msg_id = msg['message']['message_id']
					chat_id = msg['message']['chat']['id']
					if 'text' in msg['message']:
						text = msg['message']['text']
					else :
						text = "null"
					new_msg.append({"update": update_id, "msg":msg_id, "chat": chat_id, "text":text})
	return new_msg

def clear_updates_messages(offset):
	null = get_updates(offset+1)
  
while(1):
	for msg in get_updates_messages():
		now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
		print("{} - new message - {} - {} - {} - {}".format(now, msg['update'], msg['msg'], msg['chat'], msg['text']))
		if(msg['text'] == "/help"):
			repondre_message(msg['msg'], msg['chat'], help_text)
		else:
			repondre_message(msg['msg'], msg['chat'], unknow_text)
		clear_updates_messages(msg['update'])
