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
        self._mode = args.modes # server global user modes
        self.user = args.ident # *!<this>@*
        if args.real_name: self.real_name = args.real_name # "*!*@* <this>" (data given from /whois query)
        channels = args.channels.split(',')
        self.connect(args.server, port=args.port, channel=channels, use_ssl=args.ssl, password=args.server_password)
        if args.password: self.identify(args.password) # nickserv identification
        self.trigger = args.trigger # trigger for manual bot functions (ex: ~quit)
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
    
    def on_message(self, event): # will execute whenever a message ("PRIVMSG <user|channel> :<message>") is recieved by the bot, both channel and query
        if event.message.find(self.trigger) == 0: # ex: ~quit or ~join #channel
            calluserfunc(self, event) # call predefined function in /functions (should be able to modify them while the bot is running)
        
    def reqadmin(self, funcname, host): # add function to "admin only" list, also performs admin check if the function wasn't already in the list
        if funcname not in self.adminfuncs:
            self.adminfuncs.append(funcname)
            return host in self.admins
        else:
            return true
    
    def calluserfunc(self, event):
        line = event.params[0][len(self.trigger):]
        command = line.split(None,1)[0]
        if not path.exists('./functions/'+command+'.py'): return
        if command in self.adminfuncs and event.host not in self.admins: # admin privs check
           self.send_message(event.source,"This function is restricted to administrators only.")
           return
        
        try:
            args = line.split(None,1)[1]
        except IndexError:
            args = ''
        # dynamic import/call of the function
        exec "import functions.{0} as bot{0}".format(command)
        exec "bot{0}.main(self, args, event)".format(command)

if __name__ == '__main__':
    args = parseargs.getargs() # get command line arguments
    
    spirebot = SpireBot(args) # instantiate bot class
    
    if not args.no_ident_server:
        identd = ident.IdentServer(userid=args.ident)
        start_all()
    else:
        spirebot.start()