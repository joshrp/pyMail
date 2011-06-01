from settings import settings
class config:
	def __init__(self, db):
		self.settings = settings
		self.db = db
		self.populateDomains(True)
		
	def populateDomains(self, force=False):
		""" Parse domains from DB for speeds sake e.g. 'dev.co.uk' in settings['domains'] 
		 even though its an alias and therefore nested in the DB """
		if not 'domains' in self.settings or force:
			domains = self.db.domains.find()
			
			self.settings['domains'] = {}
			for dom in domains:
				self.settings['domains'][dom['name']] = {
					'parent': dom['name'],	
				}
				for alias in dom['alias']:
					self.settings['domains'][alias] = {
						'parent':dom['name']
					}
		return self.settings['domains']

	def __getitem__(self, var):
		return self.settings[var]