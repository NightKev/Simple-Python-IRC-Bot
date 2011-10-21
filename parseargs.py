# Copyright (c) 2011 Kevin Skusek
# The full copyright notice can be found in the file LICENSE

def getargs():
    import argparse

    parser = argparse.ArgumentParser(description='Start up the IRC bot.')
    parser.add_argument('-n','--nick', required=True, help="The nickname of the bot. Required.")
    parser.add_argument('-p','--password', default='', help="The bot's nickserv pass (only useful if the IRC server has nickname registration services). Optional.")
    parser.add_argument('-s','--server', required=True, help="The IRC server to connect to (ex: irc.rizon.net). Required.")
    parser.add_argument('--port', help="The port to connect to the IRC server on. Defaults to 6667.")
    parser.add_argument('--modes', default='+Bix', help="Initial usermodes to set on the bot upon joining the server. Defaults to '+Bix'.")
    parser.add_argument('--ident', default='SpireBot', help="The ident of the bot. Defaults to 'SpireBot'. Not used if option '--no-ident-server' is specified.")
    parser.add_argument('--no-ident-server', action='store_const', const=True, default=False, help="If you are unable to run an ident server on your computer (ie: if you can't forward port 113), then you can use this option to disable it.")
    parser.add_argument('--channels', metavar='#channel1[,#channel2[,...]]', help="Channel(s) you want the bot to join after it connects to the server; cannot be passworded channels. Optional.")
    parser.add_argument('--ssl', action='store_const', const=True, default=False, help="Connect via SSL. Optional.")
    parser.add_argument('--server-password', help="Password used to connect to the server (such as for a BNC service, or some of the livestreaming IRC servers like justin.tv/twitch.tv). Normally you won't need this.")
    parser.add_argument('--real-name', help="Sets the bot's 'real name'. Optional.")
    parser.add_argument('-t','--trigger', default='~', help="The trigger to use for bot commands (ex: '~google abc'). Defaults to ~ if not set.")
        
    return parser.parse_args()