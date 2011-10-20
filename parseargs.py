def getargs():
	import argparse

	parser = argparse.ArgumentParser(description='Start up the IRC bot.')
	parser.add_argument('-n','--nick', required=True, help="The nickname of the bot. Required.")
	parser.add_argument('-p','--pass','--password', default='', help="The bot's nickserv pass (only useful if the IRC server has nickname registration services).")
	parser.add_argument('-s','--server', required=True, help="The IRC server to connect to (ex: irc.rizon.net). Required.")
	parser.add_argument('--port', default='6667', help="The port to connect to the IRC server on. Defaults to 6667.")
	parser.add_argument('--modes', default='+Bix', help="Initial usermodes to set on the bot upon joining the server. Defaults to '+Bix'.")
	parser.add_argument('--ident', default='pybot', help="The ident of the bot. Defaults to 'pybot'.")