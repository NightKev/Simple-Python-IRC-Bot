# Copyright (c) 2011 Kevin Skusek
# The full copyright notice can be found in the file LICENSE

from __future__ import division
from ircutils import bot, ident, start_all
import parseargs
from os import path

class SpireBot(bot.SimpleBot):
    """ Main IRC bot class.
    """
    
    eventlist = ('any','welcome','ping','invite','kick','join','quit','part','nick_change','error', # ircutils.event.StandardEvent
        'message','channel_message','private_message', 'notice','channel_notice','private_notice', # ircutils.event.MessageEvent
        'ctcp','ctcp_action','ctcp_userinfo','ctcp_clientinfo','ctcp_version','ctcp_ping','ctcp_error','ctcp_time','dcc', # ircutils.event.CTCPEvent
        'reply','name_reply','list_reply','error_reply')
    
    for event_ in eventlist:
        exec """def on_{0}(self, event):
            for module in self.modules['{0}']:
                call_listener(self, event, '{0}')""".format(event_)
    
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
        self.modules = {}
        self.aliases = {}
        for event in self.eventlist:
            self.modules[event] = []
        self.loadmodule('alias') # technically, you can disable this module by deleting it, but it's somewhat critical
        
    
    def on_message(self, event): # will execute whenever a message ("PRIVMSG <user|channel> :<message>") is recieved by the bot, both channel and query
        if event.message.find(self.trigger) == 0: # ex: ~quit or ~join #channel
            calluserfunc(self, event) # call predefined function in /functions (these are invoked by an irc user directly)
        else:
            call_listener(self, event, 'message')
        
    def reqadmin(self, funcname, host): # add function to "admin only" list, also performs admin check if the function wasn't already in the list
        if funcname not in self.adminfuncs:
            self.adminfuncs.append(funcname)
            return host in self.admins
        else:
            return true
    
    def calluserfunc(self, event):
        line = event.params[0][len(self.trigger):]
        command = line.split(None,1)[0]
        if not path.exists('./functions/{0}.py'.format(command)): return
        if command in self.adminfuncs and event.host not in self.admins: # admin privs check
           self.send_message(event.source,"This function is restricted to administrators only.")
           return
        
        try:
            args = line.split(None,1)[1]
        except IndexError:
            args = ''
        # dynamic import/call of the function
        exec "import functions.{0} as botf{0}".format(command)
        exec "botf{0}.main(self, args, event)".format(command)
    
    def call_listener(self, event, type):
        pass
    
    def loadmodule(self, module):
        return
        if not path.exists('./modules/{0}.py'.format(module)): return
        exec "import modules.{0} as botm{0}".format(module)
        exec "botm{0}.main(self)"

if __name__ == '__main__':
    args = parseargs.getargs() # get command line arguments
    
    spirebot = SpireBot(args) # instantiate bot class
    
    if not args.no_ident_server:
        identd = ident.IdentServer(userid=args.ident)
        start_all()
    else:
        spirebot.start()