# Copyright (c) 2011,2012 Kevin Skusek
# The full copyright notice can be found in the file LICENSE

#from __future__ import division, print_function, unicode_literals # for later 2to3 conversion
from ircutils import bot, ident, start_all
import parseargs
#import parseconfig
import os, sys, traceback

class SpireBot(bot.SimpleBot):
    """ Main IRC bot class.
    
        [user@host ~]$ python2 spirebot.py --nick=SpireBot --server=irc.example.com
    """
    
    eventlist = ('any','welcome','ping','invite','kick','join','quit','part','nick_change','error', # ircutils.event.StandardEvent
        'message','channel_message','private_message', 'notice','channel_notice','private_notice', # ircutils.event.MessageEvent
        'ctcp','ctcp_action','ctcp_userinfo','ctcp_clientinfo','ctcp_version','ctcp_ping','ctcp_error','ctcp_time','dcc', # ircutils.event.CTCPEvent
        'reply','name_reply','list_reply','error_reply') # ostensibly, ircutils.event.ReplyEvent
    
    for event_ in eventlist: # create handlers for all possible ircutils builtin events
        if event_ == 'message': continue
        exec """def on_{0}(self, event):
            for module in self.modules['{0}']:
                self.call_listeners(event, '{0}')""".format(event_)
    
    def __init__(self,args):
        bot.SimpleBot.__init__(self, args.nick)
        self._mode = args.modes # server global user modes
        self.user = args.ident # *!<this>@*
        if args.real_name: self.real_name = args.real_name # "*!*@* <this>" (such as given in response to a /whois query)
        channels = args.channels.split(',')
        self.connect(args.server, port=args.port, channel=channels, use_ssl=args.ssl, password=args.server_password)
        self.server = args.server
        if args.password: self.identify(args.password) # nickserv identification
        self.trigger = args.trigger # trigger for commands (ex: ~quit)
        self.admins = []
        try:
            if os.path.exists('admins.txt'):
                adminfile = open('admins.txt','r')
                for user in adminfile:
                    self.admins.append(user.replace("\n",''))
            else:
                adminfile = open('admins.txt','w')
                adminfile.write('')
                adminfile.close()
        except IOError:
            traceback.print_exc() #DEBUG
            exit(1)
        
        self.corecmds = ['load','unload','reload','quit'] # commands required for the proper operation of the bot
        self.admincmds = self.corecmds
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
        
        self.init_aliases()
    
    def on_message(self, event): # will execute whenever a message ("PRIVMSG <user|channel> :<message>") is recieved by the bot, both channel and query
        if event.message.find(self.trigger) == 0: # ex: ~quit or ~join #channel
            self.call_user_cmd(event)
        
        self.call_listeners(event, 'message')
    
    # TODO: find a[n easy] way for modules to add their own commands without needing a .py file for each
    def call_user_cmd(self, event):
        admincmd = False
        alias = ''
        line = event.params[0][len(self.trigger):]
        command = line.split(None,1)[0]
        if command in self.aliases:
            alias = command
            command = self.aliases[command]
        # TODO: change this so it supports disabling of commands
        # TODO: re-add old method of checking for admin commands in addition to current method
        if command == '__init__': return
        elif not command.isalnum():
            command = command.translate(None,("/", "\\", ":", "(", ")", "<", ">", "|", "?", "*", "."))
        cexist = os.path.exists('./commands/{0}.py'.format(command))
        if not cexist:
            acexist = os.path.exists('./commands/admin/{0}.py'.format(command))
            if not acexist:
                return
            elif event.host not in self.admins:
                self.send_message(event.target,"This function is restricted to administrators only.")
                return
            else:
                admincmd = True
        
        try:
            args = line.split(None,1)[1]
        except IndexError:
            args = ''
        
        # dynamic import/call of the function
        try:
            if not admincmd:
                exec "import commands.{0} as botcmd{0}".format(command)
            else:
                exec "import commands.admin.{0} as botcmd{0}".format(command)
            
            exec "self.c_{0} = botcmd{0}".format(command)
            exec "self.c_{0}.main(self, args, event, alias)".format(command)
        except ImportError:
            self.send_message(event.target, "An error occurred while trying to perform command '{0}'.".format(command))
            traceback.print_exc() #DEBUG
    
    def call_listeners(self, event, type):
        "Execute listeners of the specified event type."
        for module in self.modules[type]:
            exec "self.m_{0}.main(event)".format(module)
    
    def load_module(self, module):
        "Import and initialize a module."
        err = ''
        if module == '__init__':
            return "Invalid module name."
        elif not module.isalnum():
            module = module.translate(None,("/", "\\", ":", "(", ")", "<", ">", "|", "?", "*", "."))
        
        if not os.path.exists('./modules/{0}.py'.format(module)):
            return "Module does not exist."
        
        try:
            exec "import modules.{0} as botm{0}".format(module)
            exec "self.m_{0} = botm{0}".format(module)
            exec "self.m_{0}.init(self)".format(module)
        except ImportError:
            traceback.print_exc() #DEBUG
            return "An error occured while trying to load module '{0}'.".format(module)
    
    def add_module(self, modname, type):
        "Add a module to the list of active modules so that it may be executed."
        self.modules[type].append(modname)
    
    def init_aliases(self):
        "Add the pre-defined list of aliases to the running bot."
        if not os.path.exists('aliases.txt'):
            try:
                aliasfile = open('aliases.txt','w')
                aliasfile.write('')
                aliasfile.close()
            except IOError:
                traceback.print_exc() #DEBUG
                exit(1)
        
        try:
            aliasfile = open('aliases.txt','r')
        except IOError:
            traceback.print_exc() #DEBUG
            exit(1)
        
        for line in aliasfile:
            try:
                alias = alias.replace('\n','')
                alias = line.split(',')
                self.aliases[alias[0]] = alias[1]
            except IndexError:
                traceback.print_exc() #DEBUG

if __name__ == '__main__':
    args = parseargs.getargs()
    #config = parseconfig.getconfig()
    
    spirebot = SpireBot(args)
    
    if args.use_identd_server:
        id = 'SpireBot'
        idport = 113
        if args.ident:
            id = args.ident
        if args.identd_port:
            idport = args.identd_port
        identd = ident.IdentServer(port=idport, userid=id)
        identd.start()
    
    spirebot.start()