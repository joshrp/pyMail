from twisted.internet import reactor
from pymail.database import database
from pymail.logging import console
from pyMail.smtp import protocol, queue, delivery
import config

db = database.instance()

conf = config.config(db)
if ( conf['services']['smtp']['on'] ):	
	console.log('Starting SMTP on port %s' % (conf['services']['smtp']['port']))
	
	deliv = delivery.deliveryAgent(db.messages)
	queue = queue.queue(db.queue, deliv)	
	queue.restore()   
	
	reactor.listenTCP(conf['services']['smtp']['port'], protocol.serverFactory(conf['services']['smtp'], queue))
	
if ( conf['services']['smtps']['on'] ):	
	reactor.listenSSL(conf['services']['smtps']['port'], protocol.serverFactory(conf['services']['smtps'], queue))

if ( conf['services']['imap']['on'] ):	
	reactor.listenTCP(conf['services']['imap']['port'], protocol.factory(conf['services']['imap'], queue))

reactor.run()


