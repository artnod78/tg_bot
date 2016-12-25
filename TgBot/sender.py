# -*- coding: UTF-8 -*-
import sys
from TgLib import TgSender

token = '<token>'

def main():
	sender = TgSender(token, sys.argv[1])
	sender.send(sys.argv[2])

if __name__ == '__main__':
	main()