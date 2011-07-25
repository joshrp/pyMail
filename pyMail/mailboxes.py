from address import Address
from logging import console
from config import config
class mailboxes:
	db = config.instance.db.mailboxes
	def __init__(self, domain):
		pass
		
	@staticmethod
	def byId(ids):
		boxes = {}
		for box in mailboxes.db.find({'_id': {'$in': ids}}):
			if len(box['children']) > 0:
				box['flags'].append('\Haschildren')
			boxes[int(box['_id'])] = box	
		return boxes
		
	@staticmethod	
	def _searchParent(box, boxes):
		if 'parent' in box and '/' not in box['name']:
			
			return mailboxes._searchParent(parent, boxes) + '/' +box['name']
		return box['name']
