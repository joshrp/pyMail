from pyMail.smtp import protocol
from twisted.internet import reactor
mail = protocol.Sender()
mail.addRCPT('paystey2k5@gmail.com')
f = open('log.log')
mail.setDATA(f.read())
f.close()
d = mail.send('gmail-smtp-in.l.google.com')
def printmeh(res):
	reactor.stop()
	print res
	
d.addCallback(printmeh)
reactor.run()

