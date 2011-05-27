from address import Address
class messageTransport:
    """Provides access and helpers to a message that is in transport
        These are only composed of 
        _to: [] of User's
        _from: User
        _body: main text body and (currently) attachments
        _headers: [] of headers split for each one
    """
    def __init__(self, _from=None, _to=None, helo=''):
        if _from is None or _to is None:
            raise('No sender and Receiver!?')
        self.data = []
        self.helo = helo
        self.headers = []
        self._from = _from
        self._to = _to
    
    def isLocal(self):
        return self._to.fullAddress[-8:] == '@dev.com'
        
    def addLine(self, data):
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
