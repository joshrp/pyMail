from twisted.protocols import basic
from twisted.internet import protocol, reactor, defer
from message import messageTransport
from address import Address
from pyMail.logging import console
from StringIO import StringIO
import dns.resolver

class serverProtocol(basic.LineOnlyReceiver):	
	
	def connectionMade(self):
		self.fulldata = []
		self._body = []
		self.loginUser = None
		self.loginPass = None
		self.mode = 'COMMAND'
		self.peer = self.transport.getPeer().host
		console.log('Connection Received from: %s on Port %s' % (self.peer, self.transport.getPeer().port))
		
		self.sendCode(220, 'mail.dev.com ESMTP pyMail')
	
	def lineReceived(self, line):
		self.fulldata.append(line)  
		console.log( self.peer+ ' (C): ' + line)
		func = getattr(self, 'state_%s' % (self.mode), None)
		func(line)
			
	def sendCode(self, code, message, cont=False):
		if cont:
			resp = '%s%s\n' % (code, message)
		else:
			resp = '%s %s\n' % (code, message)
		self.transport.write(resp)
		console.log('Me(S): %s' % (resp[:-1]))
		
	def state_COMMAND(self, command):
		"""Called when awaiting new command form client"""
		if command.strip() == '':
			self.consecutiveErrors = self.consecutiveErrors + 1;
			if self.consecutiveErrors == 10:
				self.sendCode(221, 'Too Many Consectutive Protocol Errors (Your talking shit, Go Away)')
				self.do_QUIT()
			return False;
		self.consecutiveErrors = 0
		splits = command.split(None)
		method = getattr(self, 'do_' + splits[0].upper(), None)
		if method is not None:
			method(splits[1:])
		else:
			self.sendCode(500, 'Command Not Implemented')
			
	def do_EHLO(self, args):
		self.helo = ' '.join(args)
		self.sendCode(250, '%s - %s' % (self.settings['welcome'], ' '.join(args)))
		self.sendCode(250, '-AUTH LOGIN', True)
		self.sendCode(250, '-AUTH PLAIN', True)
		
	def do_AUTH(self, args):
		self.mode = 'AUTH'
		self.sendCode(334, 'VXNlcm5hbWU6')
	
	def state_AUTH(self, value):
		if self.loginUser is None:
			self.loginUser = value
			self.sendCode(334, 'UGFzc3dvcmQ6')
		else:
			self.mode = 'COMMAND'
			self.loginPass = value
			self.sendCode(235, 'authenticated')
			
	def do_QUIT(self, args):
		self.sendCode(221, "Goodbye!!")
		self.transport.loseConnection()	   
	
	def do_RSET(self, args):
		self.mode = 'COMMAND'
		self.body = []
		self.fulldata = []
		self.sendCode(250, ' Ok I\'ve Reset')
	
	def do_MAIL(self, args):		
		splits = args[0].split(':')		
		if (splits[0].upper() == 'FROM'):
			"""TODO:: Mail from check"""
			self._from = Address(splits[1])
		self.sendCode(250, 'Ok Sending as from %s' % (self._from))
	
	def do_RCPT(self, args):
		splits = args[0].split(':')
		if ( splits[0] == 'TO' ):
			"""TODO::check rcpt agaist domains and whatnot"""
			addr = Address(splits[1])
			valid, reason = addr.isValidEmail()
			if not valid:
				self.sendCode(500, 'Unnaccepted: Not a valid Address %s' % reason)
			else:
				self._to = addr 
				self.sendCode(250, 'Ok %s Added to Receipient list' % (self._to))
		
	
	def do_DATA(self, args):
		if self._from is not None and self._to is not None:
			self.mode = 'DATA'
			self.message = messageTransport(self._from, self._to, self.helo)
			self.sendCode(354, 'End data with <CR><LF>.<CR><LF>')
		else:
			self.sendCode(503, 'Need to have Valid MAIL FROM and RCPT TO')
			
	def state_DATA(self, data):
		"""Called on new lines when in DATA mode"""
		if data == '.':
			self.mode = 'COMMAND'
			self.sendCode(250, " OK Queued as some message I'll neer deliver :)")
			self.queue.add(self.message)
			return
		"""remove buffed periods"""		
		if( len(data) > 0 and data[0] == '.' ): 
			data = data[1:]
		
		self.message.addLine(data)

		
class serverFactory(protocol.ServerFactory):
	protocol = serverProtocol
	def __init__(self, settings, queue, portal=None):
		self.settings = settings
		self.portal = portal
		self.queue = queue
		
	def buildProtocol(self, addr):
		p = protocol.ServerFactory.buildProtocol(self, addr)
		p.settings = self.settings
		p.portal = self.portal
		p.queue = self.queue
		return p

class clientProtocol(basic.LineOnlyReceiver):
	

	def connectionMade(self):
		self._continuation = []
		self._stopLog = False
		self._expected = [220]
		self._goodResponse = self.do_helo
		self._badResponse = self.no_connection
		self.peer = self.transport.getPeer().host
		console.log('has connection to %s' % self.peer)
		
	def no_connection(self, resp):
		console.log( 'Server issud a bad connection response')
		
	def lineReceived(self, line):
		code = int(line[0:3])
		console.log('%s(S): %s' % (self.peer, line))
		
		if(line[3] == '-'):
			self._continuation.append(line)
			return True
			
		if ( code in self._expected):
			result = self._goodResponse(code, line[4:])
			if isinstance(result, tuple):
				msg = result[1]
				result = result[0]
			
			self._continuation = []
			
		else:
			result, msg = self._badResponse(code, line[4:])
		
		if result:
			return True
		else:
			console.log( 'something buggered up, dropping connection')
			self.factory.messageFailed(msg)
			self.closeConnection()
	
	def sendLine(self, msg):
		if not self._stopLog:
			console.log('Me(C): %s' % msg)
		self.transport.write(msg + '\r\n')
	
	def connectionFailed(self):
		console.log('Couldn\'t Connect to Server')
	
	def closeConnection(self):
		console.log('Closing Connection')
		self.transport.loseConnection()		

	def do_helo(self, code, resp):
		self._expected = [250]
		self._goodResponse = self.do_mail
		self._badResponse = self.no_ehlo
		self.sendLine('ehlo localTest.com')
		return True
	
	def no_ehlo(self, code, resp):
		return False, 'Got Bad Ehlo Repsonse of: %s - %s, should probably implement helo?' % (code, resp)
		
	def do_mail(self, code, resp):
		if ( (self._continuation) > 0 ):
			#parse abilities
			pass
		
		self.sendLine('MAIL FROM: %s' % self.factory.mailFrom.fullAddress)
		self._expected = [250]
		self._goodResponse = self.start_RCPT
		self._badResponse = self.mail_rejected
		return True
	
	def mail_rejected(self, code, resp):
		return False, 'Server Rejected Mail From with: %s' % resp
		
	def start_RCPT(self, code, resp):
		self.addresses = iter(self.factory.rcpt)
		self._rejectedRCPT = []
		self._acceptedRCPT = []
		self._expected = xrange(0, 1000)
		self._goodResponse = self.RCPT_or_DATA
		#should never fire a bad response because of range of expected codes
		self._lastAddress = None
		self.RCPT_or_DATA(0, '')
		return True
	
	def RCPT_or_DATA(self, code, resp):
		if self._lastAddress is not None:
			if ( code != 250 ):
				self._rejectedRCPT.append(self._lastAddress)
				console.log('%s: RCPT TO Address Rejected - %s' % (self.peer, self._lastAddress))
			else:
				self._acceptedRCPT.append(self._lastAddress)
			
		try: 			
			self._lastAddress = self.addresses.next()			
		except StopIteration:
			if ( len(self._acceptedRCPT) == 0 ):
				return False, 'All given RCPTs were rejected'
			#start data command we're out of addresses
			self.start_data(code, resp)
		else:
			self.sendLine('RCPT TO: %s' % self._lastAddress.fullAddress)
		return True
			
	def start_data(self, code, resp):
		self.sendLine('DATA')
		self._expected = [354]
		self._goodResponse = self.do_data
		self._badResponse = self.no_data_start
		return True
		
	def no_data_start(self, code, resp):
		return False, 'Server Rejected starting Data command with: %s - %s' % (code, resp)
		
	def do_data(self, code, resp):
		self._stopLog = False
		s = basic.FileSender()
		d = s.beginFileTransfer(self.factory.data, self.transport, self.transformChunk)
	
		self._stopLog = False
		def ebTransfer(err):
			console.log( 'Oh Dear')

		d.addCallbacks(self.transferComplete, ebTransfer)
		return True
		
	def transferComplete(self, lastsent):
		self._expected = [250]
		self._goodResponse = self.message_complete
		self._badResponse = self.fail_data
		if lastsent != '\n':
			line = '\r\n.'
		else:
			line = '.'
		self.sendLine(line)	
		
	def transformChunk(self, chunk):
		return chunk.replace('\n', '\r\n').replace('.\r\n', '..\r\n')
		
	def message_complete(self, code, resp):
		self.factory.messageDelivered()
		self.closeConnection()
		return True
	
	def fail_data(self, code, resp):
		return False, 'Message Failed after data sent with: %s' % resp

class ESMTPSender(protocol.ClientFactory):
	protocol = clientProtocol
	
	def __init__(self, d):
		self.d = d		
		
	def buildProtocol(self, addr):
		p = protocol.ClientFactory.buildProtocol(self, addr)
		p.d = self.d
		return p
		
	def messageFailed(self, msg):
		self.d.errback(msg)
		
	def messageDelivered(self):
		self.d.callback(':)')
	
class Sender:

	def __init__(self):	
		
		self._from = ''
		self._to = []
		pass
	
	def addRCPT(self, arg):
		self._to.append(arg) 
	
	def setDATA(self, data):
		if not isinstance(data, file):
			data = StringIO(data)
		self.data = data
		
	def send(self):
		d = defer.Deferred()
		factory = ESMTPSender(d)
		factory.mailFrom = self._from
		factory.rcpt = self._to
		factory.data = self.data

		host = None
		records = dns.resolver.query(self._to[0].domain, 'MX')
		current = 100
		for rec in records:
			if host is None or rec.preference < current:	
				current = rec.preference
				host = str(rec.exchange)
				
		console.log('Initiating client connetion to: %s' % host)
		reactor.connectTCP(host, 25, factory, 3)
		return d

