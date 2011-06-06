from twisted.internet import reactor
import sys
from pyMail.database import database
from pyMail.logging import console

from pyMail.config import config
db = database.instance()

config = config(db)

if ( config.services['smtp']['on'] ):
	from pyMail.smtp import queue, delivery, protocol	
	console.log('Starting SMTP on port %s' % (config.services['smtp']['port']))
	
	deliv = delivery.deliveryAgent(db.messages)
	queue = queue.queue(db.queue, deliv)	
	queue.restore()   
	
	reactor.listenTCP(config.services['smtp']['port'], protocol.serverFactory(config.services['smtp'], queue))
	
if ( config.services['smtps']['on'] ):	
	reactor.listenSSL(config.services['smtps']['port'], protocol.serverFactory(config.services['smtps'], queue))

if ( config.services['imap']['on'] ):
	from pyMail.imap import protocol
	console.log('Starting IMAP on port %s' % config.services['imap']['port'])	
	reactor.listenTCP(config.services['imap']['port'], protocol.serverFactory(config.services['imap']))

reactor.run()


