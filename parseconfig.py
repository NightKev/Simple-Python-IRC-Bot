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

def setdefaults():
    import os.path

    if not os.path.exists("defaults.cfg"):
        import ConfigParser
        config = ConFigParser.SafeConfigParser()

        c = "Misc Settings"
        config.add_section(c)
        config.set(c, "Identd Server Port", "113")
        config.set(c, "Use Identd Server", "false")

        c = "IRC Server"
        config.add_section(c)
        config.set(c, "Default Channels", "")
        config.set(c, "Use SSL", "false")
        config.set(c, "Server Password", "")
        config.set(c, "Port", "6667")
        config.set(c, "Server", "")

        c = "Bot Settings"
        config.add_section(c)
        config.set(c, "Autoload Modules", "true")
        config.set(c, "Trigger", "~")
        config.set(c, "User Modes", "+Bix")
        config.set(c, "Real Name", "SpireBot")
        config.set(c, "Ident", "SpireBot")
        config.set(c, "Password", "")
        config.set(c, "Username", "SpireBot")



def getconfigs():
    import ConfigParser

    config = ConfigParser.SafeConfigParser()
    config.readfp(open("settings.cfg"))

