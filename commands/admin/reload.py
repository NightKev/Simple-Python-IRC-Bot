# Copyright (c) 2012 Kevin Skusek
# The full copyright notice can be found in the file LICENSE

def main(self, args, event, alias):
    try:
        type = args.split(None,1)[0]
    except IndexError:
        self.send_message(event.target,"You must specify a module type.")
        return
    
    if type == 'c' or type == "command":
        type = 'c'
    elif type == 'm' or type == "module":
        type = 'm'
    else:
        self.send_message(event.target,"You must specify a valid module type.")
    
    try:
        module = args.split(None,2)[1]
    except IndexError:
        self.send_message(event.target,"You must specify a module or command.")
        return
    
    try:
        exec "reload(self.{0}_{1})".format(type,module)
        self.send_message(event.target,"Module reloaded successfully!")
    except:
        self.send_message(event.target,"This module has not yet been loaded (or does not exist).")