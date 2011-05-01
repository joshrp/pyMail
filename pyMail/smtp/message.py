class messageTransport:
    """Provides access and helpers to a message that is in transport
        These are only composed of 
        _to: [] of User's
        _from: User
        _body: main text body and (currently) attachments
        _headers: [] of headers split for each one
    """
    def __init__(self, _from=None, _to=None):
        if _from is None or _to is None:
            raise('No sender and Receiver!?')
        self.data = []
        self.headers = []
        self._from = _from
        self._to = _to
    
    def isLocal(self):
        return True;
        
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
            'to': self._to,
            'from': self._from,
            'headers': self.headers
        }
    
    def __setstate__(self, obj):
        self.data = obj['data']
        self._to = obj['to']
        self._from = obj['from']
        self.headers = obj['headers']
        print self._to
class message:
    pass