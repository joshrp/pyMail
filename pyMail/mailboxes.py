from address import Address
from logging import console
from config import config
class mailboxes:
	db = config.instance.db.mailboxes
	def  __init__(self, domain):
		pass
		
	@staticmethod
	def byId(ids):
		"""
			return all mailboxes that match the IDs given
			Main use: finding all mailboxes for a user from their array of IDs
		"""
		#boxes = {}
		boxes = []
		for box in mailboxes.db.find({'_id': {'$in': ids}}):
			if 'children' in box and len(box['children']) > 0:
				box['flags'].append('\Haschildren')
			#box['_id'] = int(box['_id'])
			#boxes[box['_id']] = box
			boxes.append(box)	
		return boxes
