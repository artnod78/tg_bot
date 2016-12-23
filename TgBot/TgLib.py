# -*- coding: UTF-8 -*-
import requests, json, datetime, shutil, os

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

class TgFiler:
	"""Classe définissant un fileserver pour un bot Telegram caractérisée par :
	- son token
	- une liste d'utilisateur
	- un répertoire de stockage"""
	
	white_list = []
	current_dir = {}
	command_list = ['cd', 'ls', 'pwd', 'mkdir', 'rm', 'get', 'help','start']
	
	def __init__(self, token, users, homedir):
		self.bot = TgBot(token)
		self.home_dir = os.path.realpath(homedir)
		for user in users:
			self.white_list.append(user)
			self.current_dir[user] = os.path.join(homedir,user)
			if not os.path.exists(self.current_dir[user]):
				os.makedirs(self.current_dir[user])
			
	def exec_Cd(self, param, user):
		if param == '..':
			tmp_dir = os.path.split(self.current_dir[user])[0]
			if os.path.isdir(tmp_dir):
				self.current_dir[user] = tmp_dir
		else:
			tmp_dir = os.path.join(self.current_dir[user] ,param)
			if os.path.isdir(tmp_dir):
				self.current_dir[user] = tmp_dir
		
		test_path = os.path.realpath(self.current_dir[user])+'\\'
		real_path = os.path.realpath(os.path.join(self.home_dir,user))+'\\'
		if not test_path.startswith(real_path):
			self.current_dir[user] = os.path.join(self.home_dir,user)
		return self.current_dir[user]
			
	def exec_Ls(self, user):
		path = self.current_dir[user]
		entries = os.listdir(path)
		list_file = []
		list_dir = []
		text = 'Path: ' + path.replace(self.home_dir, '') + '\n'
		for entry in entries:
			if os.path.isfile(os.path.join(path , entry)):
				list_file.append(entry)
			elif os.path.isdir(os.path.join(path , entry)):
				list_dir.append(entry)
		if len(list_file) == 0:
			text = text + '0 file\n'
		elif len(list_file) == 1:
			text = text + '1 file\n'
		else:
			text = text + str(len(list_file)) + ' files\n'
		if len(list_dir) == 0:
			text = text + '0 directory\n'
		elif len(list_dir) == 1:
			text = text + '1 directory\n'
		else:
			text = text + str(len(list_dir)) + ' directories\n'	
		for entry in entries:
			if os.path.isfile(os.path.join(path , entry)):
				text = text + ' \n\t\t\t\t📄' + entry
			elif os.path.isdir(os.path.join(path , entry)):
				text = text + ' \n\t\t\t\t📂' + entry		
		return text
		
	def exec_Pwd(self, user):
		return self.current_dir[user].replace(self.home_dir, '')
	
	def exec_Mkdir(self, param, user):
		path = os.path.join(self.current_dir[user],param)
		test_path = os.path.realpath(path)+'\\'
		real_path = os.path.realpath(os.path.join(self.home_dir,user))+'\\'
		if test_path.startswith(real_path):
			if not os.path.exists(path):
				os.makedirs(path)
				return 'Success'
			return 'Already exist'
		return 'Fail'
	
	def exec_Rm(self, param, user):
		path = os.path.join(self.current_dir[user],param)
		test_path = os.path.realpath(path)+'\\'
		real_path = os.path.realpath(os.path.join(self.home_dir,user))+'\\'
		if test_path.startswith(real_path) and test_path != real_path:
			if os.path.exists(path):
				if os.path.isfile(path):
					os.remove(path)
				elif os.path.isdir(path):
					shutil.rmtree(path)
				return 'Success'
			return 'Doesn\' t exist'
		return 'Fail'
		
	def exec_Get(self, param, user):
		path = os.path.join(self.current_dir[user],param)
		test_path = os.path.realpath(path)+'\\'
		real_path = os.path.realpath(os.path.join(self.home_dir,user))+'\\'
		if test_path.startswith(real_path):
			if os.path.exists(path):
				if os.path.isfile(path):
					return True
		return False
		
	def exec_Help(self):
		return """Voici la liste des commandes disponible:
/cd <dir> - Change directory to <dir>
/ls - List items in current directory
/pwd - Show path of current directory
/mkdir - Make directory
/rm <item> - Remove file or directory
/get <file> - Get file\n"""

	def exec_Command(self, msg):
		for cmd in msg.get_Command():
			command = cmd['cmd']
			param = cmd['param']
			user = msg.get_Username()
			if command in self.command_list:
				if(command == 'cd'):
					reply = self.exec_Cd(param, user).replace(self.home_dir, '')
				elif(cmd['cmd'] == 'ls'):
					reply = self.exec_Ls(user)
				elif(command == 'pwd'):
					reply = self.exec_Pwd(user)
				elif(command == 'mkdir'):
					reply = self.exec_Mkdir(param, user)
				elif(command == 'rm'):
					reply = self.exec_Rm(param, user)
				elif(command == 'get'):
					if self.exec_Get(param, user):
						self.bot.send_Document(msg, os.path.join(self.current_dir[user],param), param)
						reply = None
					else:
						reply = 'File Error'
				elif(command == 'help'):
					reply =  self.exec_Help()
				elif(command == 'start'):
					reply = 'Bienvenue.\nTu peux essayer /help pour obtenir de l\'aide'
			else:
				reply = 'Désolé je ne comprends pas la demande.\nTu peux essayer /help pour obtenir de l\'aide.'
			self.bot.reply_Message(msg, reply)
		return cmd
	
	def download_File(self, msg):
		fileId = msg.get_DocumentId()
		fileName = msg.get_DocumentName()
		user = msg.get_Username()
		path = os.path.join(current_dir[user], fileName)
		self.bot.get_File(fileId, path)
		reply = 'Fichier Téléchargé: ' + fileName
		self.bot.reply_Message(msg, reply)
		return fileName

	def run(self):
		reply = ''
		msg_list = self.bot.get_Message()
		for message in msg_list:
			msg = TgMsg(message)
			if msg.is_Edited() == False:
				if msg.get_Username() in self.white_list:
					if msg.have_Document():
						reply = self.download_File(msg)
					elif msg.have_Command():
						reply = self.exec_Command(msg)
				else:
					self.bot.reply_Message(msg, 'Access Denied')
					reply = 'Access Denied'
			self.bot.clear_Message(msg)
			print("{} - {} - {} - {} - {}".format(
				msg.get_Date(), 
				msg.get_UpdateId(), 
				msg.get_Username(), 
				msg.get_ChatId(), 
				reply
				))
	
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		