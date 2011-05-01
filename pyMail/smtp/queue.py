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
       
        self.saveState()
        
    def startLoop(self):
        print 'Starting Loop'
        d = threads.deferToThread(self.deliverQueue)   
        def err(x):
            print x
        d.addErrback(err)     
        return d
        
    def deliverQueue(self):        
        for q in self.queue:
            print 'Processing: %s' % (q['message']._from)
            if ( q['reAttempt'] < time.time() and q['reAttempt'] != 0 ):
                continue            
            res = self.delivery.attempt(q['message'])
            res.addCallback(self.messageSuccess)
            res.addErrback(self.messageFailure)
    
    def messageSuccess(self, args):
        message, note = args
        print 'WIIIIIIN : from %s to %s \nDelivery note: %s' % (message._from, message._to, note)
        
    def messageFailure(self, message):
        print 'ZOMG FAAAAIL: from %s to %s' % (message._from, message._to)
    
    def restore(self):
        for m in self.db.find({}).sort([['added', pymongo.ASCENDING], ['attempt.time', pymongo.ASCENDING]]):
            m['message'] = cPickle.loads( str( m['message'] ) )
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
        for m in self.queue[:]:
            m['message'] = cPickle.dumps(m['message'])
            lst.append(m)
        db.insert(lst)
    