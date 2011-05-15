from twisted.internet import reactor
from pymail.database import database
from pyMail.smtp import protocol, queue, delivery
from config import settings 
import cPickle

db = database.instance()

if ( settings['services']['smtp']['on'] ):    
    print 'Starting SMTP on port %s' % (settings['services']['smtp']['port'])
    
    deliv = delivery.deliveryAgent(db.messages)
    queue = queue.queue(db.queue, deliv)    
    queue.restore()   
    
    reactor.listenTCP(settings['services']['smtp']['port'], protocol.serverFactory(settings['services']['smtp'], queue))
    
if ( settings['services']['smtps']['on'] ):    
    reactor.listenSSL(settings['services']['smtps']['port'], protocol.serverFactory(settings['services']['smtps'], queue))

if ( settings['services']['imap']['on'] ):    
    reactor.listenTCP(settings['services']['imap']['port'], protocol.factory(settings['services']['imap'], queue))
    
reactor.run()
