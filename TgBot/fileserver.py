# -*- coding: UTF-8 -*-
from TgLib import TgFiler

token = "<token>"
white_list = ['<username>',]
home_dir = r'<path>'

def main():
	filserver = TgFiler(token, white_list, home_dir)
	while(1):
		filserver.run()

if __name__ == '__main__':
	main()