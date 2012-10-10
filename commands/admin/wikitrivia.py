# Copyright (c) 2012 Kevin Skusek
# The full copyright notice can be found in the file LICENSE

from ircutils import events

class TriviaInfo():
    category = ""
    started = False
    debug = False
    
class Trivia(events.EventListener): # I think I'm doing this wrong... it's so confusing!
    answer = ''
    
    def notify(self, client, event):
        if client.wikitrivia.started == False:
            return
        
        # TODO: Figure out how to use event listeners/handlers/etc
    
    def test(self, client, event):
        title = get_title(client.wikitrivia.category)
        article = get_article(title)
        if not article:
            article = "XML Parse Error"
        
        if title[7] == 't': # aka: title[7:24] == "tools.wikimedia.de"
            self.send_message(event.target, "Error getting article title")
        else:
            # TODO: Everything
            pass

    def get_title(self, cat):
        cat = cat.translate(None,"|") # "|" is the category separator and we only want one category
        
        import urllib
        cat = urllib.urlencode({"key":cat})
        cat = cat[4:]

        import urllib2
        
        req = urllib2.Request("http://tools.wikimedia.de/~erwin85/randomarticle.php?lang=en&family=wikipedia&categories={0}&namespaces=0&subcats=1&d=10".format(cat))
        req.add_header("User-Agent","Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.289 Version/12.02") # Needs a proper user agent otherwise 403 error
        
        data = urllib2.urlopen(req)
        url = data.geturl()
        title = url[30:]
        return title

    def get_article(self, title):
        import urllib2
        article = urllib2.urlopen("http://en.wikipedia.org/w/api.php?action=query&titles={0}&export&exportnowrap".format(title))
        article = article.read()
        
        import xml.etree.ElementTree as ET
        article_xml = ET.fromstring(article)
        
        # TODO(?): Make this future-proof against changes in the location of the 'text' element in the article XML
        try:
            if article_xml[1][3][6].tag[42:] == "text":
                article_text = article_xml[1][3][6].text
            else:
                article_text = article_xml[1][3][7].text
        except IndexError:
            return ""
        
        return article_text

def verify_category(cat):
    import urllib, urllib2
    import xml.etree.ElementTree as ET
    exist = False
    
    cat_e = urllib.urlencode({"key":cat})
    cat_e = cat_e[4:]
    
    wiki = urllib2.urlopen("http://en.wikipedia.org/w/api.php?action=query&format=xml&list=allcategories&aclimit=1&acprefix={0}".format(cat_e))
    wiki = wiki.read()
    wiki = ET.fromstring(wiki)
    try:
        if wiki[0][0][0].text.lower() == cat.lower():
            exist = True
    except IndexError:
        pass
    
    return exist

def main(self, args, event, alias):
    if not hasattr(self, "wikitrivia"):
        self.wikitrivia = TriviaInfo() # used to store persistent session information
    
    try:
        action = args.split(None,1)[0].lower()
    except IndexError:
        self.send_message(event.target, "You must specify an action to take. Use '{0}wikitrivia help' for more information.".format(self.trigger))
        return
    
    if action == "help":
        self.send_message(event.target, "Currently unimplemented.") # I'm such a helpful guy!
    elif action == "debug":
        try:
            toggle = args.split(None,1)[1].lower()
        except IndexError:
            toggle = ''
        
        if toggle == "on" or toggle == "true":
            self.wikitrivia.debug = True
        elif toggle == "off" or toggle == "false":
            self.wikitrivia.debug = False
        else:
            self.wikitrivia.debug = not self.wikitrivia.debug
        
        self.send_message(event.target, "Debug status set to '{0}'.".format(str(self.wikitrivia.debug)))
    elif action == "setcat":
        try:
            cat = args.split(None,1)[1]
        except IndexError:
            self.send_message(event.target, "You must specify a category.")
        
        if verify_category(cat):
            self.wikitrivia.category = cat
        else:
            self.send_message(event.target, "This is not a valid English Wikipedia category.")
    elif action == "start":
        if not self.wikitrivia.category:
            self.send_message(event.target, "No category has been chosen.")
            return
        
        self.register_listener("channel_message",Trivia()) # is this right?