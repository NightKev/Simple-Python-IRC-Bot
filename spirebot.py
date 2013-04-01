# This file is part of SpireBot.
#
# SpireBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SpireBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SpireBot.  If not, see <http://www.gnu.org/licenses/>.

import os
# import sys
import traceback

from ircutils import bot, ident, start_all

import parseargs
import parseconfig


class SpireBot(bot.SimpleBot):
    """ Main IRC bot class.

        [user@host ~]$ python2 spirebot.py --nick=SpireBot --server=irc.example.com
    """

    eventlist = ('any', 'welcome', 'ping', 'invite', 'kick', 'join', 'quit', 'part', 'nick_change', 'error',  # ircutils.event.StandardEvent
        'message', 'channel_message', 'private_message', 'notice', 'channel_notice', 'private_notice',  # ircutils.event.MessageEvent
        'ctcp', 'ctcp_action', 'ctcp_userinfo', 'ctcp_clientinfo', 'ctcp_version', 'ctcp_ping', 'ctcp_error', 'ctcp_time', 'dcc',  # ircutils.event.CTCPEvent
        'reply', 'name_reply', 'list_reply', 'error_reply')  # unknown, ircutils.event.ReplyEvent?

    for event_ in eventlist:  # create handlers for all possible ircutils builtin events
    #    if event_ == 'message': continue
        exec """def on_{0}(self, event):
            for module in self.modules['{0}']:
                self.call_listeners(event, '{0}')""".format(event_)

    def __init__(self, settings):
        bot.SimpleBot.__init__(self, settings.nick)
        self._mode = settings.modes  # server global user modes
        self.user = settings.ident  # *!<this>@*
        if settings.real_name: self.real_name = settings.real_name  # "*!*@* <this>" (such as given in response to a /whois query)
        channels = settings.channels.split(',')
        self.connect(settings.server, port=settings.port, channel=channels, use_ssl=settings.ssl, password=settings.server_password)
        self.server = settings.server
        if settings.password: self.identify(settings.password)  # nickserv identification
        self.trigger = settings.trigger  # trigger for commands (ex: ~quit)
        self.admins = []
        try:
            if os.path.exists('admins.txt'):
                adminfile = open('admins.txt', 'r')
                for user in adminfile:
                    self.admins.append(user.replace("\n", ''))
            else:
                adminfile = open('admins.txt', 'w')
                adminfile.write('')
                adminfile.close()
        except IOError:
            traceback.print_exc()  # DEBUG
            exit(1)

        self.admincmds = []
        self.modules = {}
        self.aliases = {}
        for event in self.eventlist:
            self.modules[event] = []

        if settings.load_modules:
            for dirpath, dirnames, fnames in os.walk('modules/'):
                if dirpath != 'modules/':
                    break
                for fname in fnames:
                    self.load_module(fname)
                break

        self.init_aliases()

    # def on_message(self, event): # will execute whenever a message ("PRIVMSG <user|channel> :<message>") is recieved by the bot, both channel and query
    #    if event.message.find(self.trigger) == 0: # ex: ~quit or ~join #channel
    #        self.call_user_cmd(event)
    #
    #    self.call_listeners(event, 'message')

    # TODO: switch entirely to a module-based loading system
    def call_user_cmd(self, event):
        admincmd = False
        alias = ''
        line = event.params[0][len(self.trigger):]
        command = line.split(None, 1)[0]
        if command in self.aliases:
            alias = command
            command = self.aliases[command]
        # TODO: change this so it supports disabling of commands
        # TODO: re-add old method of checking for admin commands in addition to current method
        if command == '__init__': return
        elif not command.isalnum():
            command = command.translate(None, ("/", "\\", ":", "(", ")", "<", ">", "|", "?", "*", "."))
        cexist = os.path.exists('./commands/{0}.py'.format(command))
        if not cexist:
            acexist = os.path.exists('./commands/admin/{0}.py'.format(command))
            if not acexist:
                return
            elif event.host not in self.admins:
                self.send_message(event.target, "This function is restricted to administrators only.")
                return
            else:
                admincmd = True

        try:
            args = line.split(None, 1)[1]
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
            traceback.print_exc()  # DEBUG

    def call_listeners(self, event, evtype):
        "Execute listeners of the specified event evtype."
        for module in self.modules[evtype]:
            exec "self.m_{0}.main(event)".format(module)

    def load_module(self, module):
        "Import and initialize a module."
        err = ''
        if module == '__init__':
            return "Invalid module name."
        elif not module.isalnum():
            module = module.translate(None, ("/", "\\", ":", "(", ")", "<", ">", "|", "?", "*", "."))

        if not os.path.exists('./modules/{0}.py'.format(module)):
            return "Module does not exist."

        try:
            exec "import modules.{0} as botm{0}".format(module)
            exec "self.m_{0} = botm{0}".format(module)
            exec "self.m_{0}.init(self)".format(module)
        except ImportError:
            traceback.print_exc()  # DEBUG
            return "An error occured while trying to load module '{0}'.".format(module)

    def add_module(self, modname, modtype):
        "Add a module to the list of active modules so that it may be executed."
        self.modules[modtype].append(modname)

    def init_aliases(self):
        "Add the pre-defined list of aliases to the running bot."
        return  # TODO: move this into the Core module
        if not os.path.exists('aliases.txt'):
            try:
                aliasfile = open('aliases.txt', 'w')
                aliasfile.write('')
                aliasfile.close()
            except IOError:
                traceback.print_exc()  # DEBUG
                exit(1)

        try:
            aliasfile = open('aliases.txt', 'r')
        except IOError:
            traceback.print_exc()  # DEBUG
            exit(1)

        for line in aliasfile:
            try:
                alias = line.replace('\n', '').split(',')
                self.aliases[alias[0]] = alias[1]
            except IndexError:
                traceback.print_exc()  # DEBUG

if __name__ == '__main__':
    args = parseargs.getargs()
    config = parseconfig.BotConfig().config

    for key in args:

        pass

    spirebot = SpireBot(args)

    if args.use_identd_server:
        ident = 'SpireBot'
        idport = 113
        if args.ident:
            ident = args.ident
        if args.identd_port:
            idport = args.identd_port
        identd = ident.IdentServer(port=idport, userid=ident)
        start_all()
    else:
        spirebot.start()
