from pyMail.smtp import protocol

mail = protocol.Sender()

d = mail.send('mail.google.com')
def printmeh(res):
	print res
	
d.addCallback(printmeh)

