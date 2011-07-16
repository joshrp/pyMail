from pyMail.config import config
class Address:
	def __init__(self, addr):
		self.fullAddress = addr
		if (addr[0] == '<') != (addr[-1] == '>'):
			raise TypeError('Unbalanced "<>"')
		if (addr[0] == '<') and (addr[-1] == '>'):
			addr = addr[1:-1]
		
		split = addr.split('@')		
		self.user = split[0]
		self.domain = split[1]
	
	def isValidEmail(self):
		addr = self.fullAddress
		if ( addr.index('@') in [0, len(addr)-1, -1] ) :
			return [False, 'No @ ?']
		return [True, '']
	
	def isLocal(self):
		conf = config.instance
		return conf.ResolveDomain(self.domain) != False
	 
	def __str__(self):
		return self.fullAddress	
		

