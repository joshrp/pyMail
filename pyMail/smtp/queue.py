import cPickle, pymongo, time
from pyMail.logging import console
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
		console.log( 'New Item in Queue: From %s To %s' % (msg._from, msg._to) )
		self.startLoop()
		
	def startLoop(self):
		if len(self.queue) > 0:
			d = threads.deferToThread(self.deliverQueue)	 
			def err(x):
				reactor.stop()
				print x
			d.addErrback(err)	 
			return d
		return True
		
	def deliverQueue(self): 
		i = 0		
		for q in self.queue:
			console.log( 'Processing: Queue Item %s from %s to %s' % (i, q['message']._from, q['message']._to)	)
			if ( q['reAttempt'] < time.time() and q['reAttempt'] != 0 ):
				continue			
			try:
				res = self.delivery.attempt(q['message'], i)
				res.addCallback(self.messageSuccess)
				res.addErrback(self.messageFailure)
			except:
				 import sys, traceback
				 inf = sys.exc_info()
				 console.log('Exception in delivery thread: \n%s' % inf[0])
				 console.log('Trace: \n' + '\n'.join(traceback.format_tb(inf[2])))
			
			i = i + 1
		self.saveState()
	
	def messageSuccess(self, args):
		id, message, queueId = args
		self.queue.pop(queueId)
		console.log('WIIIIIIN : from %s to %s \nMessage ID: %s' % (message._from.fullAddress, message._to.fullAddress, id))
		self.saveState()
		
	def messageFailure(self, args):
		id, message, queueId = args
		console.log('ZOMG FAAAAIL: from %s to %s' % (message._from, message._to))
	
	def restore(self):
		for m in self.db.find().sort([['added', pymongo.ASCENDING], ['attempt.time', pymongo.ASCENDING]]):
			m['message'] = cPickle.loads( str(m['message']) )			
			m['reAttempt'] = 0
			self.queue.append(m)
			
		console.log( 'Restored Queue from db state')
		console.log( '%s Total Queued Items ' % len(self.queue))
		self.startLoop()
		
	def saveState(self, db=None):
		if db is None:
			db = self.db
		db.remove()
		lst = []
		"""Make full copy of OBJECT and list so nothing in the queue is altered"""
		for m in range(len(self.queue)):
			obj = dict(self.queue[m])
			obj['message'] = cPickle.dumps(obj['message'])
			lst.append(obj)
		if len(lst) > 0:
			db.insert(lst)
	
