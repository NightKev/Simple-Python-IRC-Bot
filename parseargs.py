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

""" If a commandline argument is specified, it will override the corresponding option in settings.cfg
"""

def getargs():
    import argparse

    parser = argparse.ArgumentParser(description="Start up the IRC bot.")

    botargs = parser.add_argument_group("Bot Settings", "Various options related to the bot itself.")
    botargs.add_argument('-n', '--nick', help="The nickname of the bot.")
    botargs.add_argument('-p', '--password', help="The bot's nickserv pass (only useful if the IRC server has nickname registration services and you have registered the nickname used by the bot).")
    botargs.add_argument('--ident', help="The 'ident' of the bot. Used in the second part of the 'user!<ident>@host' scheme. Defaults to 'SpireBot'.")
    botargs.add_argument('--real-name', help="Sets the bot's 'real name'.")
    botargs.add_argument('-t', '--trigger', help="The trigger to use for bot commands (ex: '!google abc' or '.weather 90210'). Defaults to '~' if not set.")
    botargs.add_argument('--modes', help="Initial usermodes to set on the bot upon joining the server. Defaults to '+Bix'.")
    botargs.add_argument('--no-autoload-modules', action='store_const', const=True, default=False, help="Stops the bot from automatically loading all of the modules from the 'modules/' directory on start-up. Defaults to false.")

    serverargs = parser.add_argument_group("IRC Server", "Options related to the IRC server you are connecting to.")
    serverargs.add_argument('-s', '--server', help="The IRC server to connect to (ex: irc.example.com).")
    serverargs.add_argument('--port', help="The port to connect to the IRC server on. Defaults to 6667.")
    serverargs.add_argument('--server-password', help="Password used to connect to the server (such as for a BNC service, or some of the livestreaming IRC servers). Normally you won't need this.")
    serverargs.add_argument('--ssl', action='store_const', const=True, default=False, help="Connect via SSL. Defaults to off.")
    serverargs.add_argument('--channels', metavar='#channel1[,#channel2[,...]]', help="Channel(s) you want the bot to join after it connects to the server; cannot be passworded channels.")

    miscargs = parser.add_argument_group("Misc Settings")
    miscargs.add_argument('--use-identd-server', action='store_const', const=True, default=False, help="Runs an identd server in parallel with the bot. Can in some cases speed up the connection process. Requires port 113 to be available for use by the bot. May require some port forwarding/redirecting.")
    miscargs.add_argument('--identd-port', help="Set a port other than 113 to be used locally by the identd server before being forwarded to 113 by a router.")


    return parser.parse_args()
