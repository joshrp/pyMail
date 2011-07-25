from settings import settings
from database import database
from logging import console
class config:
	instance = None
	def __init__(self, db, force=False):	
		if config.instance is None or force:		
			self.settings = settings
			self.db = db
			config.instance = self
	
	def ResolveDomain(self, name):
		res = self.db.domains.find({'$or': [{'name': name}, {'alias': name}]})
		if res.count() == 1:
			return Domain(res[0])
		else:
			return False
	
	def ResolveAccount(self, name):	
		import account, address
		addr = address.Address(name)
		if not addr.isLocal:
			return False
		domain = self.ResolveDomain(addr.domain)
		if domain == False:
			return False
		if domain.hasUser(addr.user):
			return account.Account(addr, domain, domain.users[addr.user])
		else:
			return False	
				
	def __getattr__(self, var):
		return self.settings[var]
		
class Domain:
	def __init__(self, dom):
		self.db = database.instance().domains
		self.__dict__ = dom
	
	def hasUser(self, user):
		return user in self.users
	
