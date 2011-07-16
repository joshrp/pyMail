from address import Address
from config import config
class Accounts:
	def __init__(self, domain):
		conf = config.instance
		if isinstance(domain, str):
			domain = conf.ResolveDomain(addr.domain)
		
	
	def __getitem__(self, key):
		if isinstance(key, str):
			#search posible users for this name
		elif isinstance(key, int):
			#grab user with int key
		#return Account(id)
