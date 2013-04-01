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

class BotConfig:
    def __init__(self, restore_defaults=False):
        self.set_defaults(restore_defaults)
        # self.config = self.get_configs()

    def set_defaults(self, restore_defaults):
        import os.path

        if not os.path.exists("defaults.cfg") or restore_defaults:
            import ConfigParser
            config = ConfigParser.SafeConfigParser()

            c = "Bot Settings"
            config.add_section(c)
            config.set(c, "Username", "SpireBot")
            config.set(c, "Password", "")
            config.set(c, "Ident", "SpireBot")
            config.set(c, "Real Name", "SpireBot")
            config.set(c, "User Modes", "+Bix")
            config.set(c, "Trigger", "~")
            config.set(c, "Autoload Modules", "true")

            c = "IRC Server"
            config.add_section(c)
            config.set(c, "Server", "")
            config.set(c, "Port", "6667")
            config.set(c, "Server Password", "")
            config.set(c, "Use SSL", "false")
            config.set(c, "Default Channels", "")

            c = "Misc Settings"
            config.add_section(c)
            config.set(c, "Use Identd Server", "false")
            config.set(c, "Identd Server Port", "113")

            try:
                defaultConfigFile = open("defaults.cfg", "w")
                config.write(defaultConfigFile)
                defaultConfigFile.close()
            except IOError:
                print("Error opening 'defaults.cfg', make sure directory permissions are properly set.")
                exit(1)

            try:
                if not os.path.exists("settings.cfg") or restore_defaults:
                    userConfigFile = open("settings.cfg", "w")
                    config.write(userConfigFile)
                    userConfigFile.close()
            except IOError:
                print("Error opening 'settings.cfg', make sure directory permissions are properly set.")
                exit(1)



    def get_configs(self):
        import ConfigParser

        config = ConfigParser.SafeConfigParser()
        config.readfp(open("defaults.cfg"))
        config.read("settings.cfg")

if __name__ == '__main__':
    BotConfig()
