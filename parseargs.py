# Copyright (c) 2011,2012 Kevin Skusek
# The full copyright notice can be found in the file LICENSE

def getargs():
    import argparse

    parser = argparse.ArgumentParser(description='Start up the IRC bot.')
    parser.add_argument('-n','--nick', required=True, help="The nickname of the bot. Required.")
    parser.add_argument('-p','--password', default='', help="The bot's nickserv pass (only useful if the IRC server has nickname registration services and you have registered the nickname used by the bot).")
    parser.add_argument('-s','--server', required=True, help="The IRC server to connect to (ex: irc.example.com). Required.")
    parser.add_argument('--port', help="The port to connect to the IRC server on. Defaults to 6667.")
    parser.add_argument('--modes', default='+Bix', help="Initial usermodes to set on the bot upon joining the server. Defaults to '+Bix'.")
    parser.add_argument('--ident', default='SpireBot', help="The 'ident' of the bot. Used in the second part of the 'user!<ident>@host' scheme. Defaults to 'SpireBot'.")
    parser.add_argument('--use-identd-server', action='store_const', const=True, default=False, help="Runs an identd server in parallel with the bot. Can in some cases speed up the connection process. Requires port 113 to be available for use by the bot. May require some port forwarding/redirecting.")
    parser.add_argument('--identd-port', help="Set a port other than 113 to be used locally by the identd server before being forwarded to 113 by a router.")
    parser.add_argument('--channels', metavar='#channel1[,#channel2[,...]]', help="Channel(s) you want the bot to join after it connects to the server; cannot be passworded channels.")
    parser.add_argument('--ssl', action='store_const', const=True, default=False, help="Connect via SSL.")
    parser.add_argument('--server-password', help="Password used to connect to the server (such as for a BNC service, or some of the livestreaming IRC servers). Normally you won't need this.")
    parser.add_argument('--real-name', help="Sets the bot's 'real name'.")
    parser.add_argument('-t','--trigger', default='~', help="The trigger to use for bot commands (ex: '~google abc'). Defaults to ~ if not set.")
    parser.add_argument('--load-modules', action='store_const', const=True, default=False, help="Load all modules from the 'modules/' directory on start-up.")
        
    return parser.parse_args()