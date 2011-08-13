from address import Address
from pyMail.logging import console
from config import config
class Account:
	def __init__(self, addr, domain=None, preLoad=None):
		conf = config.instance
		self.authd = False

			
		if isinstance(addr, int):
			pass
			#it's an id, grab from db based on 
		elif isinstance(addr, Address) == False:
			addr = Address(addr)
			if preLoad is not None:
				self.__dict__ = preLoad
			else:
				pass #pull data from db	
				
		if domain is None:
			domain = conf.ResolveDomain(addr.domain)
			
		if domain.hasUser(addr):
			console.log('Retrived User: %s@%s' % (addr.user, addr.domain))
		
	def AuthenticateBasic(self, secret):
		if self.password == secret.hexdigest():
			self.authd = True
		else:
			self.authd = False
		return self.authd

	def findMailbox(self, name=None, root=None):
		parents = []
		if name is None:
			return False
			
		if '/' in name:
			parents = name.split('/');
			name = parents[-1]
		
		for par in parents:
			if par == '%':
				pass
			elif par == '*':
				pass #Oh shi
			elif type(par) != str:
				break
			elif par in self.mailboxes:
				self.mailboxes[par]
		return True
			
			
		
	def __getattr__(self, var):
		if var == 'mailboxes':
			import mailboxes
			self.mailboxes = mailboxes.mailboxes.byId(self.mailboxIds)
			return self.mailboxes
		raise AttributeError, var
