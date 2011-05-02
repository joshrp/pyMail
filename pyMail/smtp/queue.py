import cPickle, pymongo, time
from twisted.internet import defer, reactor, threads
from message import messageTransport

class queue:
    def __init__(self, db, delivery):
        self.db = db
        self.delivery = delivery
        self.queue = []
        
    def add(self, msg=None):
        if msg is None:
            raise('Add blank email to queue!?')
        elif not isinstance(msg, messageTransport):
            try:
                msg = messageTransport(msg)
            except:
                raise('Dunno what you want me to add to the queue here?')

        self.queue.append({
            'message': msg,
            'added': time.time(),
            'attmepts':[],
            'reAttempt': 0
        })
        self.saveState()
        print 'New Item in Queue: From %s To %s' % (msg._from, msg._to)
        self.startLoop()
        
    def startLoop(self):
        print 'Starting Loop'
        d = threads.deferToThread(self.deliverQueue)   
        def err(x):
            print x
        d.addErrback(err)     
        return d
        
    def deliverQueue(self): 
        i = 0       
        for q in self.queue:
            print 'Processing: %s' % (q['message']._from)	
            if ( q['reAttempt'] < time.time() and q['reAttempt'] != 0 ):
                continue            
            res = self.delivery.attempt(q['message'], i)
            res.addCallback(self.messageSuccess)
            res.addErrback(self.messageFailure)
            i = i + 1
        self.saveState()
    
    def messageSuccess(self, args):
        id, message, queueId = args
        self.queue.pop(queueId)
        print 'WIIIIIIN : from %s to %s \nMessage ID: %s' % (message['_from'], message['_to'], id)
        
    def messageFailure(self, message):
        print message
        print 'ZOMG FAAAAIL: from %s to %s' % (message['_from'], message['_to'])
    
    def restore(self):

        for m in self.db.find().sort([['added', pymongo.ASCENDING], ['attempt.time', pymongo.ASCENDING]]):
            m['message'] = cPickle.loads( str(m['message']) )            
            m['reAttempt'] = 0
            self.queue.append(m)
            
        print 'Restored Queue from db state'
        print '%s Total Queued Items ' % (len(self.queue))
        self.startLoop()
        
    def saveState(self, db=None):
        if db is None:
            db = self.db
        db.remove()
        lst = []
        #print type(self.queue[0]['message'])
        """Make full copy of OBJECT and list so nothing in the queue is altered"""
        for m in range(len(self.queue)):
            obj = dict(self.queue[m])
            obj['message'] = cPickle.dumps(obj['message'])
            lst.append(obj)
        #print type(self.queue[0]['message'])
        if len(lst) > 0:
            db.insert(lst)
    
