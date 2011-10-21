# Copyright (c) 2011 Kevin Skusek
# The full copyright notice can be found in the file LICENSE

from ircutils import bot, ident, start_all
import parseargs
from os import path

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
        self.trigger = args.trigger
        self.admins = []
        try:
            if path.exists('./admins.txt'):
                adminfile = open('admins.txt','r')
                for user in adminfile:
                    self.admins.append(user)
            else:
                adminfile = open('admins.txt','w')
                adminfile.write('')
                adminfile.close()
                
        except IOError:
            print("Unable to open admins.txt. Make sure the bot directory is read/write enabled for the appropriate user(s).")
        
        self.adminfuncs = []
    
    def on_message(self, event):
        if event.message.find(self.trigger) == 0:
            calluserfunc(self, event)
        
    def reqadmin(self, funcname, host):
        if funcname not in self.adminfuncs:
            self.adminfuncs.append(funcname)
            return host in self.admins
        else:
            return true
    
    def calluserfunc(self, event):
        line = event.params[0][len(self.trigger):]
            command = line.split(None,1)[0]
            if not path.exists('./functions/'+command+'.py'): return
            if command in self.adminfuncs and event.host not in self.admins:
               self.send_message(event.source,"This function is restricted to administrators only.")
               return
            
            try:
                args = line.split(None,1)[1]
            except IndexError:
                args = ''
            
            exec "import functions.{0} as bot{0}".format(command)
            exec "bot{0}.main(self, args, event)".format(command)

if __name__ == '__main__':
    args = parseargs.getargs()
    
    spirebot = SpireBot(args)
    
    if not args.no_ident_server: 
        identd = ident.IdentServer(userid=args.ident)
        start_all()
    else:
        spirebot.start()