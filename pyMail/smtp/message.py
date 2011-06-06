from address import Address
import re
class messageTransport:
	"""Provides access and helpers to a message that is in transport
		These are only composed of 
		_to: User
		_from: User
		_mode: The mode of adding data to message, header/body
		_data: All of the data 
		_body: main text body and (currently) attachments
		_headers: [] of headers split for each one
	"""
	InvisibleLine = re.compile(r'^[\t\s]+$', re.IGNORECASE)
	def __init__(self, _from=None, _to=None, helo=''):
		if _from is None or _to is None:
			raise('No sender and Receiver!?')
		self.data = []
		self.helo = helo
		self.headers = []
		self._from = _from
		self._to = _to
		self._mode = 'header'
		
	def addLine(self, data):
		if self._mode == 'header':
			if self.InvisibleLine.match(data):
				pass
		elif self._mode == 'body':
			pass
		self.data.append(data)
	
	def getBody(self):
		return '\n'.join(self.data)
	
	def addHeader(self, header):
		#add to header var
		return True
		
	def getHeaders(self, header):
		return '\n'.join(self.headers)
	
	def getFull(self):
		return '%s\n%s' % (self.getHeaders, self.getBody)
		"""TODO::Seperate Attachments from body"""
	
	def __getstate__(self):
		return {
			'data': self.data,
			'to': self._to.fullAddress,
			'from': self._from.fullAddress,
			'headers': self.headers,
			'helo': self.helo
		}
	
	def __setstate__(self, obj):
		self.data = obj['data']
		self._to = Address(obj['to'])
		self._from = Address(obj['from'])
		self.headers = obj['headers']
		self.helo = obj['helo']
		
class message:
	pass
