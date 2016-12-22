# -*- coding: UTF-8 -*-
import os, shutil
from TgLib import TgBot, TgMsg

token = "<token>"
white_list = ['Artnod', 'lacarpe']
home_dir = os.path.realpath('E:/fileserver/')

command_list = ['cd', 'ls', 'pwd', 'mkdir', 'rm', 'get', 'help']
current_dir = {}

def create_UserDir(user_dir):
	if not os.path.exists(user_dir):
		os.makedirs(user_dir)
	
def init_CurrentDir():
	for user in white_list:
		current_dir[user] = os.path.join(home_dir,user)
		create_UserDir(current_dir[user])

def exec_Cd(param, user):
	if param == '..':
		tmp_dir = os.path.split(current_dir[user])[0]
		if os.path.isdir(tmp_dir):
			current_dir[user] = tmp_dir
	else:
		tmp_dir = os.path.join(current_dir[user] ,param)
		if os.path.isdir(tmp_dir):
			current_dir[user] = tmp_dir
	
	test_path = os.path.realpath(current_dir[user])+'\\'
	real_path = os.path.realpath(os.path.join(home_dir,user))+'\\'
	if not test_path.startswith(real_path):
		current_dir[user] = os.path.join(home_dir,user)
	
def exec_Ls(user):
	path = current_dir[user]
	entries = os.listdir(path)
	list_file = []
	list_dir = []
	text = 'Path: ' + current_dir[user].replace(home_dir, '') + '\n'
	
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
	
def exec_Pwd(user):
	return current_dir[user].replace(home_dir, '')
	
def exec_Mkdir(param, user):
	path = os.path.join(current_dir[user],param)
	test_path = os.path.realpath(path)+'\\'
	real_path = os.path.realpath(os.path.join(home_dir,user))+'\\'
	if test_path.startswith(real_path):
		if not os.path.exists(path):
			os.makedirs(path)
			return 'Success'
		return 'Already exist'
	return 'Fail'
			
def exec_Rm(param, user):
	path = os.path.join(current_dir[user],param)
	test_path = os.path.realpath(path)+'\\'
	real_path = os.path.realpath(os.path.join(home_dir,user))+'\\'
	if test_path.startswith(real_path) and test_path != real_path:
		if os.path.exists(path):
			if os.path.isfile(path):
				os.remove(path)
			elif os.path.isdir(path):
				shutil.rmtree(path)
			return 'Success'
		return 'Doesn\' t exist'
	return 'Fail'		
	
def exec_Get(param, user):
	path = os.path.join(current_dir[user],param)
	test_path = os.path.realpath(path)+'\\'
	real_path = os.path.realpath(os.path.join(home_dir,user))+'\\'
	if test_path.startswith(real_path):
		if os.path.exists(path):
			if os.path.isfile(path):
				return True
	return False
					
def exec_Command(bot, msg):
	# pour chaque commande	
	for cmd in msg.get_Command():
		command = cmd['cmd']
		param = cmd['param']
		user = msg.get_Username()
		# si la commande existe
		if command in command_list:
			# on affiche une ligne pour faire joli
			afficher_ligne(msg, command)
			if(command == 'cd'):
				exec_Cd(param, user)
				reply = current_dir[user].replace(home_dir, '')
			elif(cmd['cmd'] == 'ls'):
				reply = exec_Ls(user)
			elif(command == 'pwd'):
				reply = exec_Pwd(user)
			elif(command == 'mkdir'):
				reply = exec_Mkdir(param, user)
			elif(command == 'rm'):
				reply = exec_Rm(param, user)
			elif(command == 'get'):
				if exec_Get(param, user):
					bot.send_Document(msg, os.path.join(current_dir[user],param), param)
					reply = None
				else:
					reply = 'File Error'
			elif(command == 'help'):
				reply =  """Voici la liste des commandes disponible:
/cd <dir> - Change directory to <dir>
/ls - List items in current directory
/pwd - Show path of current directory
/mkdir - Make directory
/rm <item> - Remove file or directory
/get <file> - Get file\n"""
		else:
			reply = "Désolé je ne comprends pas la demande.\nTu peux essayer /help pour obtenir de l'aide"
		bot.reply_Message(msg, reply)

def download_File(bot, msg):
	fileId = msg.get_DocumentId()
	fileName = msg.get_DocumentName()
	user = msg.get_Username()
	path = os.path.join(current_dir[user], fileName)
	bot.get_File(fileId, path)
	afficher_ligne(msg, msg.get_DocumentName())
	reply = 'Fichier Téléchargé: ' + fileName
	bot.reply_Message(msg, reply)

def afficher_ligne(msg, txt):
	print("{} - {} - {} - {} - {}".format(
		msg.get_Date(), 
		msg.get_UpdateId(), 
		msg.get_Username(), 
		msg.get_ChatId(), 
		txt
		))
		
def main():
	# on initialise les dossier utilisateur
	init_CurrentDir()
	# on initialise le bot
	bot = TgBot(token)
	while(1):
		# recupere la liste de tout les messages avec des commandes
		msg_list = bot.get_Message()
		
		# traitement pour chaque message recupere
		for message in msg_list:
			# on initialise le message
			msg = TgMsg(message)
			if msg.is_Edited() == False:
				# si l'username est dans la white_list
				if msg.get_Username() in white_list:
					# si le message contien un document
					if msg.have_Document():
						download_File(bot, msg)
					# si le message contient des commandes
					elif msg.have_Command():
						exec_Command(bot, msg)
				else:
					bot.reply_Message(msg, 'Access Denied')
			# on efface le message
			bot.clear_Message(msg)

if __name__ == '__main__':
	main()
