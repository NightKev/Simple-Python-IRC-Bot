# Copyright (c) 2011 Kevin Skusek
# The full copyright notice can be found in the file LICENSE

#from __future__ import division, print_function, unicode_literals
from ircutils import bot, ident, start_all
# try:
    # from . import parseargs, alias
# except ValueError:
    # import parseargs, alias
import parseargs, alias
import os

class SpireBot(bot.SimpleBot):
    """ Main IRC bot class.
    
        [user@host ~]$ python2 spirebot.py --nick=SpireBot --server=irc.example.com # minimum required shell parameters
    """
    
    eventlist = ('any','welcome','ping','invite','kick','join','quit','part','nick_change','error', # ircutils.event.StandardEvent
        'message','channel_message','private_message', 'notice','channel_notice','private_notice', # ircutils.event.MessageEvent
        'ctcp','ctcp_action','ctcp_userinfo','ctcp_clientinfo','ctcp_version','ctcp_ping','ctcp_error','ctcp_time','dcc', # ircutils.event.CTCPEvent
        'reply','name_reply','list_reply','error_reply') # ostensibly, ircutils.event.ReplyEvent
    
    for event_ in eventlist: # create handlers for all possible ircutils builtin events
        if event_ == 'message': continue
        exec """def on_{0}(self, event):
            for module in self.modules['{0}']:
                call_listeners(self, event, '{0}')""".format(event_)
    
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
            if os.path.exists('./admins.txt'):
                adminfile = open('admins.txt','r')
                for user in adminfile:
                    self.admins.append(user)
            else:
                adminfile = open('admins.txt','w')
                adminfile.write('')
                adminfile.close()
        except IOError:
            import sys
            sys.stderr.write("Unable to open admins.txt. Make sure the bot directory is read/write enabled for the appropriate user(s).")
            exit(1)
        
        self.adminfuncs = []
        self.modules = {}
        self.aliases = {}
        for event in self.eventlist:
            self.modules[event] = []
        
        if args.load_modules:
            for dirpath, dirnames, fnames in os.walk('modules/'):
                if dirpath != 'modules/':
                    break
                for fname in fnames:
                    self.load_module(fname)
                break
    
    def on_message(self, event): # will execute whenever a message ("PRIVMSG <user|channel> :<message>") is recieved by the bot, both channel and query
        if event.message.find(self.trigger) == 0: # ex: ~quit or ~join #channel
            call_user_func(self, event) # call predefined function in /functions (these are invoked by an irc user directly)
        else:
            call_listeners(self, event, 'message')
        
    def req_admin(self, funcname, host): # add function to "admin only" list, also performs admin check if the function wasn't already in the list
        if funcname not in self.adminfuncs:
            self.adminfuncs.append(funcname)
            return host in self.admins
        else:
            return true
    
    def call_user_func(self, event):
        line = event.params[0][len(self.trigger):]
        command = line.split(None,1)[0]
        if command in self.aliases:
            command = self.aliases[command]
        
        if not os.path.exists('./functions/{0}.py'.format(command)) or command == '__init__': return
        
        if command in self.adminfuncs and event.host not in self.admins: # admin privs check
           self.send_message(event.target,"This function is restricted to administrators only.")
           return
        
        try:
            args = line.split(None,1)[1]
        except IndexError:
            args = ''
        
        # dynamic import/call of the function
        try:
            exec "import functions.{0} as botf{0}".format(command)
            exec "botf{0}.main(self, args, event)".format(command)
        except ImportError:
            from sys import stderr
            stderr.write("Failed to import python module '{0}.py' in 'functions/'.".format(command))
            self.send_message(event.target, "An error occurred while trying to perform command '{0}'.".format(command))
    
    def call_listeners(self, event, type):
        "Execute listeners of the specified event type."
        for module in self.modules[type]:
            exec "self.m_{0}.main(self, event)".format(module)
    
    def load_module(self, module):
        "Import and initialize a module."
        if not os.path.exists('./modules/{0}.py'.format(module)) or module != '__init__': return
        
        exec "import modules.{0} as botm{0}".format(module)
        exec "botm{0}.init(self)".format(module)
        exec "self.m_{0} = botm{0}".format(module)
    
    def add_module(self, modname, type):
        "Add a module to the list of active modules so that it may be executed."
        self.modules[type].append(modname)
    

if __name__ == '__main__':
    args = parseargs.getargs() # get command line arguments
    
    spirebot = SpireBot(args) # instantiate bot class
    
    if args.use_identd_server:
        id = 'SpireBot'
        idport = 113
        if args.ident:
            id = args.ident
        if args.identd_port:
            idport = args.identd_port
        identd = ident.IdentServer(port=idport, userid=id)
        start_all()
    else:
        spirebot.start()