# Copyright (c) 2011 Kevin Skusek
# The full copyright notice can be found in the file LICENSE

from ircutils import bot, ident, start_all
import parseargs

class SpireBot(bot.SimpleBot):
	""" Main IRC bot class.
	"""
	def __init__(self,args):
		bot.SimpleBot.__init__(self, args.nick)
		self._mode = args.modes
		self.user = args.ident
		if args.real_name: self.real_name = args.real_name
		channels = args.channels.split(',')
		self.connect(args.server, port=args.port, channel=channels, use_ssl=args.ssl, password=args.server_password)
		if args.password: self.identify(args.password)

if __name__ == '__main__':
	args = parseargs.getargs()
	
	spirebot = SpireBot(args)
	
	if not args.no_ident_server: 
		identd = ident.IdentServer(userid=args.ident)
		start_all()
	else:
		spirebot.start()