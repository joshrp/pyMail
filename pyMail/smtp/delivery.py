from twisted.internet import reactor, defer, threads

class deliveryAgent:
    def __init__(self, db):
        self.db = db          
       
    def attempt(self, message, passThruId):
        d = defer.Deferred() 
        if ( message.isLocal() ):
            #....it's HERE!
            newid = self.db.save({
                'body': message.getBody(),
                'headers': message.headers,
                '_to': message._to.fullAddress,
                '_from': message._from.fullAddress,
                'helo': message.helo,
            })
            if newid is not None:
                d.callback([newid, self.db.find({'_id': newid})[0], passThruId])
            else:
                #uh ph
                pass
        else:
            #.....it's remote?
            pass
        return d
        
        
    
        
        
        
