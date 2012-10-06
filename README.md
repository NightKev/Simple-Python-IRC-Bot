This bot requires the [IRCUtils framework][1] ([Install guide][2] and [Download][4]) and [Python 2.7.x][3]. I'll port it over to Python 3.x eventually.
[1]: http://dev.guardedcode.com/projects/ircutils
[2]: http://dev.guardedcode.com/docs/ircutils/installation.html#installing-from-source
[3]: http://python.org
[4]: http://dev.guardedcode.com/hg/ircutils/archive/b611aefde646.tar.gz

Creating bot functions
-----
Each function requires its own file (for now) (ex: `8ball.py`) in the `./commands` directory (or the `./commands/admin/` directory if you want to make it an admin-only function (second method for code-based admin-only checking Coming Soon&trade;), such as a `quit` command).  
To be executed, you must define, at a minimum, the function `main` with four parameters, like this:

    def main(self, args, event, alias):

If you want to restrict the function to only work in queries, add the following check to `main()`:

    if event.target != event.source:    # if the message was sent to a channel, event.target will be set to the channel name
        return                          # otherwise it will be the same as the nick of the user sending the message
                                        # change the "!=" into a "==" to make it work only in channels