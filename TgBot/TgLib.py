# -*- coding: UTF-8 -*-
import requests, json, datetime, shutil, os

class TgMsg:
	"""Classe définissant un message de Telegram caractérisée par :
	- son message"""

	def __init__(self, msg):
		self.__msg = msg
		
	# Check keys in json
	# Return bool
	def have_Command(self):
		if 'entities' in self.__msg[self.getKey()]:
			for cmd in self.__msg[self.getKey()]['entities']:
				if cmd['type'] == 'bot_command':
					return True
		return False
		
	def have_Document(self):
		if 'document' in self.__msg[self.getKey()]:
			return True
		return False

	def have_sticker(self):
		if 'sticker' in self.__msg[self.getKey()]:
			return True
		return False
	
	def have_Text(self):
		if 'text' in self.__msg[self.getKey()]:
			return True
		return False
		
	def is_Edited(self):
		if 'edited_message' in self.__msg:
			return True
		return False

	def isForwarded(sef):
		if 'forward_from' in self.__msg['message']:
			return True
		return False
		
	# Extract data from json
	# Return String or Integer or datetime
	def get_UpdateId(self):
		return self.__msg['update_id']
		
	def get_MessageId(self):
		return self.__msg[self.getKey()]['message_id']
		
	def get_UserId(self):
		return self.__msg[self.getKey()]['from']['id']
		
	def get_UserName(self):
		return self.__msg[self.getKey()]['from']['username']
		
	def get_ChatId(self):
		return self.__msg[self.getKey()]['chat']['id']
		
	def get_ChatName(self):
		return self.__msg[self.getKey()]['chat']['username']
		
	def get_Date(self):
		return datetime.datetime.fromtimestamp(self.__msg[self.getKey()]['date'])
		
	def get_EditDate(self):
		return datetime.datetime.fromtimestamp(self.__msg[self.getKey()]['edit_date'])
	
	def get_DocumentId(self):
		return self.__msg[self.getKey()]['document']['file_id']

	def get_DocumentName(self):
		return self.__msg[self.getKey()]['document']['file_name']
		
	def get_Text(self):
		return self.__msg[self.getKey()]['text']
		
	# Extract cmds and param
	# Return list of dict
	def get_Command(self):
		cmd_list = []
		if self.have_Command():			
			for cmd in self.__msg[self.getKey()]['entities']:
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

	# Return Json
	def getMsg(self):
		return self.__msg
		
	# Utils
	def getKey(self):
		if self.is_Edited():
			return 'edited_message'
		return 'message'
		
class TgResp():
			
	def __init__(self, resp):
		self.__resp = resp
		
	def isOk(self):
		return self.__resp['ok']
		
	def get_MessageId(self):
		return self.__resp['result']['message_id']
		
	def get_UserId(self):
		return self.__resp['result']['chat']['id']
	
	def get_UserName(self):
		return self.__resp['result']['chat']['username']
		
	def get_Date(self):
		return datetime.datetime.fromtimestamp(self.__resp['result']['date'])

	def get_Text(self):
		return self.__resp['result']['text']
		
	def get_ErrCode(self):
		return self.__resp['error_code']
		
	def get_Error(self):
		return self.__resp['description']
		
		
class TgBot:
	"""Classe définissant un bot pour Telegram caractérisée par :
	- son token
	- une liste blanche"""
	__URL = ''
	__FILE_URL = ''
	token = ''
	white_list = []
	
	def __init__(self, token, white_list):
		self.token = token
		self.__URL = 'https://api.telegram.org/bot{}/'.format(token)
		self.__FILE_URL = 'https://api.telegram.org/file/bot{}/'.format(token)
		for user in white_list:
			self.white_list.append(user)

	# API request methods
	# Return json object
	def getMe(self):
		response = requests.post(url = self.__URL + "getMe")
		return json.loads(response.content.decode("utf8"))
	
	def send_Message(self, param):
		response = requests.post(
			url = self.__URL + "sendMessage",
			data=param
		)
		js = json.loads(response.content.decode("utf8"))
		return js
		
	def get_Updates(self, param = {}):
		response = requests.post(
			url = self.__URL + "getUpdates",
			data= param
		)
		return json.loads(response.content.decode("utf8"))



	# Custom methods
	def get_Message(self):
		msg_list = []
		update_list = self.get_Updates()
		if(update_list['ok']):
			for message in update_list['result']:
				msg = TgMsg(message)
				if(msg.get_UserName() in self.white_list):
					msg_list.append(msg)
		return msg_list
		
	def get_MessageWithCommand(self):
		msg_list = []
		for msg in self.get_Message():
			if(msg.have_Command()):
				msg_list.append(msg)
		return msg_list	
		
	def get_MessageWithDocument(self):
		msg_list = []
		for msg in self.get_Message():
			if(msg.have_Document()):
				msg_list.append(msg)
		return msg_list		
		
	def reply_Message(self, msg, text):
		param = {'reply_to_message_id': msg.get_MessageId(), 'chat_id': msg.get_ChatId(), 'text': text}
		resp = self.send_Message(param)
		return TgResp(resp)
		
	def get_File(self, fileId, fullPath):
		response = requests.post(
			url = self.__URL + "getFile",
			data= {'file_id':fileId}
		)
		js = json.loads(response.content.decode("utf8"))
		response = requests.get(self.__FILE_URL + js['result']['file_path'], stream=True)
		with open(fullPath, 'wb') as f:
			shutil.copyfileobj(response.raw, f)		
		
	def send_Document(self, msg, path, name):
		url = self.__URL + "sendDocument"
		file = {'document': open(path, 'rb')}
		data = {'reply_to_message_id': msg.get_MessageId(), 'chat_id': msg.get_ChatId(), 'document': file}
		response = requests.post(url, data, files = file)
	
	def clear_Message(self, msg):
		data = {'offset':msg.get_UpdateId()+1}
		null = self.get_Updates(data)


class TgSender():

	def __init__(self, token, users):
		self.__bot = TgBot(token, users)
		
	def send(self, user, message):
		param = {'chat_id':user, 'text':message}
		resp = self.__bot.send_Message(param)
		return TgResp(resp)
	
class TgFiler:
	"""Classe définissant un fileserver pour un bot Telegram caractérisée par :
	- son token
	- une liste d'utilisateur
	- un répertoire de stockage"""
	
	__current_dir = {}
	__command_list = ['cd', 'ls', 'pwd', 'mkdir', 'rm', 'get', 'help','start']
	
	def __init__(self, token, users, homedir):
		self.__bot = TgBot(token, users)
		self.__home_dir = os.path.realpath(homedir)
		for user in users:
			self.__current_dir[user] = os.path.join(homedir,user)
			if not os.path.exists(self.__current_dir[user]):
				os.makedirs(self.__current_dir[user])
			
	
	def exec_Cd(self, param, user):
		test_path = os.path.realpath(os.path.join(self.__current_dir[user] ,param))
		real_path = os.path.realpath(os.path.join(self.__home_dir,user))+'\\'
		if str(test_path+'\\').startswith(real_path):
			if os.path.isdir(test_path):
				self.__current_dir[user] = test_path
		return self.__current_dir[user].replace(self.__home_dir, '')
			
	def exec_Ls(self, user):
		path = self.__current_dir[user]
		entries = os.listdir(path)
		list_file = []
		list_dir = []
		text = 'Path: ' + path.replace(self.__home_dir, '') + '\n'
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
		return self.__current_dir[user].replace(self.__home_dir, '')
	
	def exec_Mkdir(self, param, user):
		path = os.path.join(self.__current_dir[user],param)
		test_path = os.path.realpath(path)+'\\'
		real_path = os.path.realpath(os.path.join(self.__home_dir,user))+'\\'
		if test_path.startswith(real_path):
			if not os.path.exists(path):
				os.makedirs(path)
				return 'Success'
			return 'Already exist'
		return 'Fail'
	
	def exec_Rm(self, param, user):
		path = os.path.join(self.__current_dir[user],param)
		test_path = os.path.realpath(path)+'\\'
		real_path = os.path.realpath(os.path.join(self.__home_dir,user))+'\\'
		if test_path.startswith(real_path) and test_path != real_path:
			if os.path.exists(path):
				if os.path.isfile(path):
					os.remove(path)
				elif os.path.isdir(path):
					shutil.rmtree(os.path.realpath(path))
					if not os.path.exists(path):
						self.__current_dir[user]= os.path.join(self.__home_dir,user)
				return 'Success'
			return 'Doesn\' t exist'
		return 'Fail'
		
	def exec_Get(self, param, user):
		path = os.path.join(self.__current_dir[user],param)
		test_path = os.path.realpath(path)+'\\'
		real_path = os.path.realpath(os.path.join(self.__home_dir,user))+'\\'
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
		return_cmd = []
		for cmd in msg.get_Command():
			command = cmd['cmd']
			param = cmd['param']
			user = msg.get_UserName()
			if command in self.__command_list:
				if(command == 'cd'):
					reply = self.exec_Cd(param, user)				
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
						reply = None
						self.__bot.send_Document(msg, os.path.join(self.__current_dir[user],param), param)
					else:
						reply = 'File Error'
				elif(command == 'help'):
					reply =  self.exec_Help()
				elif(command == 'start'):
					reply = 'Bienvenue '+msg.get_UserName()+'.\nTu peux essayer /help pour obtenir de l\'aide'
				return_cmd.append({'msg':msg, 'cmd':cmd, 'reply':reply})
		return return_cmd
	
	def download_File(self, msg):
		fileId = msg.get_DocumentId()
		fileName = msg.get_DocumentName()
		user = msg.get_UserName()
		path = os.path.join(self.__current_dir[user], fileName)
		self.__bot.get_File(fileId, path)
		reply = 'Fichier Téléchargé: ' + fileName
		return reply

	def run(self):
		return_list = []
		msg_list = self.__bot.get_Message()
		for msg in msg_list:
			if msg.is_Edited() == False:
				if msg.have_Document():
					reply = self.download_File(msg)
					resp = self.__bot.reply_Message(msg, reply)
					return_list.append({'msg':msg, 'cmd':reply, 'resp':resp })
				elif msg.have_Command():
					cmds = self.exec_Command(msg)
					for cmd in cmds:
						if not cmd['reply'] == None:
							resp = self.__bot.reply_Message(cmd['msg'], cmd['reply'])
							return_list.append({'msg':msg, 'cmd':cmd['cmd'], 'resp':resp })
						else:
							return_list.append({'msg':msg, 'cmd':cmd['cmd'], 'resp':cmd['reply'] })
			self.__bot.clear_Message(msg)
		return return_list
			
			
