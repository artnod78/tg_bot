# -*- coding: UTF-8 -*-
import requests, json, datetime, shutil

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
		
	def have_Document(self):
		if('document' in self.msg['message']):
			return True
		return False

	def is_Edited(self):
		if 'edited_message' in self.msg:
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
					command = self.get_Text()[start_cmd:stop_cmd]
					
					start_param = stop_cmd + 1
					if '&' in self.get_Text()[start_param:]:
						stop_param = self.get_Text().find('&',start_param)
					else:
						stop_param = len(self.get_Text())
					param = self.get_Text()[start_param:stop_param]
					
					cmd_list.append({'cmd': command, 'param': param})
		return cmd_list

	def get_DocumentId(self):
		return self.msg['message']['document']['file_id']

	def get_DocumentName(self):
		return self.msg['message']['document']['file_name']
	
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
	FILE_URL = "not set"

	def __init__(self, token):
		self.token = token
		self.URL = "https://api.telegram.org/bot{}/".format(token)
		self.FILE_URL = "https://api.telegram.org/file/bot{}/".format(token)

	def get_Updates(self, param = {}):
		response = requests.post(
			url = self.URL + "getUpdates",
			data= param
		)
		js = json.loads(response.content.decode("utf8"))
		return js

	def send_Document(self, msg, path, name):
		url = self.URL + "sendDocument"
		file = {'document': open(path, 'rb')}
		data = {'reply_to_message_id': msg.msg['message']['message_id'], 'chat_id': msg.msg['message']['chat']['id'], 'document': file}
		response = requests.post(url, data, files = file)
	
	def get_Message(self):
		msg_list = []
		update_list = self.get_Updates()
		if(update_list['ok']):
			return update_list['result']
		
	def get_MessageWithCommand(self):
		msg_list = []
		update_list = self.get_Updates()
		if(update_list['ok']):
			for message in update_list['result']:
				msg = TgMsg(message)
				if(msg.have_Command()):
					msg_list.append(message)
		return msg_list
		
	def get_MessageWithDocument(self):
		msg_list = []
		update_list = self.get_Updates()
		if(update_list['ok']):
			for message in update_list['result']:
				msg = TgMsg(message)
				if(msg.have_Document()):
					msg_list.append(message)
		return msg_list
		
	def get_File(self, fileId, fullPath):
		response = requests.post(
			url = self.URL + "getFile",
			data= {'file_id':fileId}
		)
		js = json.loads(response.content.decode("utf8"))
		response = requests.get(self.FILE_URL + js['result']['file_path'], stream=True)
		with open(fullPath, 'wb') as f:
			shutil.copyfileobj(response.raw, f)

	def reply_Message(self, msg, text):
		response = requests.post(
			url = self.URL + "sendMessage",
			data={'reply_to_message_id': msg.msg['message']['message_id'], 'chat_id': msg.msg['message']['chat']['id'], 'text': text}
		)
		
	def clear_Message(self, msg):
		data = {'offset':msg.msg['update_id']+1}
		null = self.get_Updates(data)