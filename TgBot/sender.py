# -*- coding: UTF-8 -*-
import sys
from TgLib import TgSender

token = "<token>"

user = sys.argv[1]
message = ' '.join(map(str, sys.argv[2:]))

def main():
	sender = TgSender(token, [])
	sender.send(user, message)

if __name__ == '__main__':
	main()