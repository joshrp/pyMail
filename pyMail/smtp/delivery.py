from twisted.internet import reactor, defer, threads
from pyMail.smtp.protocol import Sender
class deliveryAgent:
	def __init__(self, db):
		self.db = db
	   
	def attempt(self, message, passThruId):
		d = defer.Deferred() 
		if ( message.isLocal() ):			
			newid = self.db.save({
				'body': message.getBody(),
				'headers': message.headers,
				'_to': message._to.fullAddress,
				'_from': message._from.fullAddress,
				'helo': message.helo,
			})
			if newid is not None:
				d.callback([newid, message, passThruId])
			else:
				#uh pass
				pass
		else:
			mail = Sender()
			mail.addRCPT(message._to)
			mail._from = message._from
			mail.setDATA(message.getBody())
			
			def cbComplete(args):
				print 'Fired'
				d.callback([0, message, passThruId])

			def ebFailed(args):
				d.errback([0, message, passThruId])
				
			sent = mail.send()
			sent.addCallback(cbComplete)
			
		return d
		
		
	
		
		
		
