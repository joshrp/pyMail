
class Address:
    def __init__(self, addr):
        self.fullAddress = addr
        self.domain = addr[ addr.find('@')+1 : -1]
    
    def isValidEmail(self):
        addr = self.fullAddress
        if ( addr.index('@') in [0, len(addr)-1, -1] ) :
            return [False, 'No @ ?']
        return [True, '']
     
    def __str__(self):
        return self.fullAddress    
        

