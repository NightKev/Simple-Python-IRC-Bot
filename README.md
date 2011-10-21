This bot requires the [IRCUtils framework][1] ([Install guide][2]) and [Python 2.7.x][3] (afaict, it should also work in Python 2.6.x (untested); it almost definitely won't work pre-2.6 though).
[1]: http://dev.guardedcode.com/projects/ircutils
[2]: http://dev.guardedcode.com/docs/ircutils/installation.html
[3]: http://python.org

Creating bot functions
-----
Each function requires its own file (ex: `quit.py`) in the `/functions` directory.
To be executed, you must define the function `main` with the parameters `self, args, event` in that order, like this:
    def main(self, args, event):

If you want to restrict the function to users with administrator privileges, you must add a call to `self.reqadmin(<name of function>)` at the top of main(), similar to this:
    def main(self, args, event):
        if not self.reqadmin('quit', event.host): # assuming the function name is 'quit'
            self.send_message(event.source,"This function is restricted to administrators only.")
            return