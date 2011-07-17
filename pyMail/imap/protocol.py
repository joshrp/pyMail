from twisted.protocols import basic
from twisted.internet import protocol, reactor, defer
from pyMail.logging import console
from pyMail.account import Account
class serverProtocol(basic.LineOnlyReceiver):
	def connectionMade(self):
		console.log('Connection Established with %s' % self.transport.getPeer().host)
		self.state = self.state_UNAUTH
		self.sendLine('OK Go Ahead')
	
	def sendLine(self, line, label='*'):
		if label is None:
			resp = '%s' % (line)	
		else:
			resp = '%s %s' % (label, line)
		console.log('(me): %s' % resp)
		self.transport.write(resp+'\r\n')	
	
	def lineReceived(self, line):
		console.log('(C): %s' % line)
		self.state(line)

	def state_AUTH(self, line):
		split = line.split(' ')
		label = split[0]
		command = split[1]
		args = split[2:]
		func = getattr(self, 'do_' + command, None)
		if func is not None:
			func(args, label)	
	
	def do_lsub(self, args, label):
		self.sendLine('LSUB (\HasChildren) "/" "INBOX"')
		self.sendLine('LSUB (\HasNoChildren) "/" "INBOX/Drafts"')
		self.sendLine('LSUB (\HasNoChildren) "/" "INBOX/Sent"')
		self.sendLine('LSUB (\HasNoChildren) "/" "INBOX/Trash"')
		self.sendLine('LSUB (\HasNoChildren) "/" "INBOX/special"')
		self.sendLine('OK LSUB Complete', label)
	
	def state_UNAUTH(self, line):
		split = line.split(' ')
		label = split[0]
		command = split[1]
		args = split[2:]
		func = getattr(self, 'do_' + command.upper(), None)
		
		if func is not None:
			func(args, label)
			
	def do_CAPABILITY(self, args, label):
		self.sendLine('CAPABILITY IMAP4REV1 AUTH=LOGIN')
		self.sendLine('OK CAPABILITY COMPLETE', label)
		
	def do_AUTHENTICATE(self, args, label):
		import base64
		self._tempUser = None
		self.state = self.state_AUTHING
		self._authLabel = label
		self._authMethod = args[0]
		self.sendLine('+ ', None)
	
	def state_AUTHING(self, line):
		import base64
		if self._authMethod == 'login':			
			user = base64.b64decode(line)
			# unicode null values seperate user and password
			if self._tempUser is None:
				self.config.ResolveAccount(user)
				if user == 'test@dev.com':
					self._tempUser = user
					self.sendLine('+ ', None)
				else:
					console.log(user)
					self.sendLine('BAD LOGIN', self._authLabel)
			else:
				if user == 'password':
					self.state = self.state_AUTH
					self.sendLine('OK Authenticated', self._authLabel)
		else:
			pass
	def do_LOGIN(self, line, label):
		self.sendLine('OK Authenticated', label)
		
class serverFactory(protocol.ServerFactory):
	protocol = serverProtocol
	
	def __init__(self, config):
		self.config = config
		
	def buildProtocol(self, addr):
		p = protocol.ServerFactory.buildProtocol(self, addr)
		p.config = self.config
		return p
