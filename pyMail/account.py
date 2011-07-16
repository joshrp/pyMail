from address import Address
from pyMail.logging import console
from config import config
class Account:
	def __init__(self, addr, domain=None, preLoad=None):
		conf = config.instance
		self.authd = False
		if preLoad is not None:
			self.data = preLoad
		else:
			pass
			#pull data from db	
		if isinstance(addr, Address) == False:
			addr = Address(addr)
		elif isinstance(addr, int):
			pass
			#it's an id, grab from db based on 	
		
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

	def __getattr__(self, var):
		return self.data[var]