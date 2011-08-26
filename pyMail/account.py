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

	def findMailbox(self, query=None, ref=''):
		
		def findMatching(group, value):
			res = []
			for item in group:
				if item['name'] == value or value == '%':
					res.append(item)
				elif value == '*':
					res.append(item)
					if 'children' in item:
						res.extend(findMatching(item['children'], '*'))
			return res
		
		res = []
		query = ref+'/'+query
		ss = query.split('/')
		#clean array of blanks
		ss = [ val for val in ss if val != '' ]
		
		for x, value in enumerate(ss):			
			if x == 0:
				group = [{'children':self.mailboxes}]
			else:
				group = res[x-1]	
			item = []
			query = value
			for g in group:
				item.extend(findMatching(g['children'], query))
			res.append( item )
			
		ret = res[-1]
		del res
		return ret
			
		
	def __getattr__(self, var):
		if var == 'mailboxes':
			import mailboxes
			self.mailboxes = mailboxes.mailboxes.byId(self.mailboxIds)
			return self.mailboxes
		elif var in self.__dict__:
			return self[var]
		raise AttributeError, var
