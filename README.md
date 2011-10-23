This bot requires the [IRCUtils framework][1] ([Install guide][2] and [Download][4]) and [Python 2.7.x][3] (afaict, it should also work in Python 2.6.x (untested), and *maybe* 2.5.x with a minimal amount of tweaking; it almost definitely won't work pre-2.5 without some non-trivial modification though).
[1]: http://dev.guardedcode.com/projects/ircutils
[2]: http://dev.guardedcode.com/docs/ircutils/installation.html#installing-from-source
[3]: http://python.org
[4]: http://dev.guardedcode.com/hg/ircutils/archive/b611aefde646.tar.gz

Creating bot functions
-----
Each function requires its own file (ex: `quit.py`) in the `/functions` directory.
To be executed, you must define the function `main` with the parameters `self, args, event` in that order, like this:

    def main(self, args, event):

If you want to restrict the function to users with administrator privileges, you must add a call to `self.reqadmin(<name of function>)` at the top of `main()`, similar to this:

    def main(self, args, event):
        if not self.req_admin('quit', event.host): # assuming the function name is 'quit'
            self.send_message(event.target,"This function is restricted to administrators only.")
            return

If you want to restrict the function to only work in queries, add the following check to `main()`:

    if event.target != event.source:    # if the message was sent to a channel, event.target will be set to the channel name
        return                          # otherwise it will be the same as the nick of the user sending the message
                                        # change the "!=" into a "==" to make it work only in channels

Quick Changelog
-----

### v0.3.2
* Finished module framework, updated readme, updated parseargs.py

### v0.3.1
* Change identd server to default off, add identd port selection argument

## v0.3
* Added most of the framework for easy addition of custom listener modules (ex: log channel messages, kickwords, etc)

## v0.2
* Added custom command framework (manual invocation of bot action upon recieving specific messages from irc users (ex: "~quit"))

## v0.1
* Create a bot that can successfully connect to IRC networks.