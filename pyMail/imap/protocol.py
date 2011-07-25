from twisted.protocols import basic
from twisted.internet import protocol, reactor, defer
from pyMail.logging import console
from pyMail.account import Account
class serverProtocol(basic.LineOnlyReceiver):
	def connectionMade(self):
		console.log('Connection Established with %s' % self.transport.getPeer().host)
		self.user = None
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
		console.log('Starting LSUB')
		for box in self.user.mailboxes:
			box = self.user.mailboxes[box]
			self.sendLine(str('LSUB (%s) "/" "%s"' % (', '.join(box['flags']), box['name'])), '*')
		self.sendLine('OK LSUB Complete', label)
	
	def state_UNAUTH(self, line):
		split = line.split(' ')
		label = split[0]
		command = split[1]
		args = split[2:]
		commands = ['authenticate', 'capability']
		if command in commands:
			getattr(self, 'do_' + command.upper(), None)(args, label)
		else:
			self.sendLine('Must be authenticated', label)
			
	def do_CAPABILITY(self, args, label):
		self.sendLine('CAPABILITY IMAP4REV1 AUTH=LOGIN')
		self.sendLine('OK CAPABILITY COMPLETE', label)
		
	def do_AUTHENTICATE(self, args, label):
		import base64
		try:
			console.log('Trying Auth type: '+args[0].upper())
			func = getattr(self, 'state_AUTH_'+args[0].upper())
		except AttributeError:
			self.sendLine('Unrecognized authentication type.')
			self.state = self.state_UNAUTH
			return False;
		self.state = func
		self._authLabel = label
		self.state(' '.join(args[1:]))
	
	def state_AUTH_LOGIN(self, args):
		"""Client passes user and pass sepertly after recieiving + from server
		base64 encoded ofc"""
		import base64, hashlib	
		if type(args) == str:
			args = args.split(' ')
				
		if len(args[0]) == 0:
			self.sendLine('+', None)
			return True
			
		line = base64.b64decode(args[0])
		if self.user is None:
			self.user = self.config.ResolveAccount(line)
			if self.user == False:
				self.sendLine('NO AUTHENTICATE Failed', self._authLabel)
				self.state = self.STATE_UNAUTH
			self.sendLine('+ ', None)
		else:
			secret = hashlib.md5()
			secret.update(line)
			if self.user.AuthenticateBasic(secret):
				self.state = self.state_AUTH
				self.sendLine('OK Authenticated', self._authLabel)
			else:
				self.sendLine('NO AUTHENTICATE Failed', self._authLabel)
				self.state = self.state_UNAUTH
		
class serverFactory(protocol.ServerFactory):
	protocol = serverProtocol
	
	def __init__(self, config):
		self.config = config
		
	def buildProtocol(self, addr):
		p = protocol.ServerFactory.buildProtocol(self, addr)
		p.config = self.config
		return p
