from twisted.internet import reactor, defer, threads

class deliveryAgent:
    def __init__(self, db):
        self.db = db          
       
    def attempt(self, message):
        d = defer.Deferred() 
        if ( message.isLocal() ):
            #....it's HERE!
            if (message._to == '<paystey2k5@gmail.com>'):
                d.callback([message, 'ZOMG I KNOW HIM!!!'])
                
        else:
            #.....it's remote?
            pass
        return d
        
        
    
        
        
        