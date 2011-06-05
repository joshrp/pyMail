from twisted.internet import reactor
import sys
from pyMail.database import database
from pyMail.logging import console
from pyMail.smtp import protocol, queue, delivery
from pyMail.config import config
sys.path.append('./')
db = database.instance()

config = config(db)

if ( config.services['smtp']['on'] ):	
	console.log('Starting SMTP on port %s' % (config.services['smtp']['port']))
	
	deliv = delivery.deliveryAgent(db.messages)
	queue = queue.queue(db.queue, deliv)	
	queue.restore()   
	
	reactor.listenTCP(config.services['smtp']['port'], protocol.serverFactory(config.services['smtp'], queue))
	
if ( config.services['smtps']['on'] ):	
	reactor.listenSSL(config.services['smtps']['port'], protocol.serverFactory(config.services['smtps'], queue))

if ( config.services['imap']['on'] ):	
	reactor.listenTCP(config.services['imap']['port'], protocol.factory(config.services['imap'], queue))

reactor.run()


